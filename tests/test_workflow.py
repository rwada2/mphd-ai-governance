"""Isolated intake/routing/review unit tests with a fixed reference date."""
from datetime import date
import unittest
from src.workflow import evaluate_proposal, validate_review

TODAY = date(2026, 10, 1)

def proposal(**changes):
    result = dict(title='Drafting public heat advisories', owner='Jordan Lee',
        department='Communications', purpose='Draft from public sources with staff verification.',
        tool='Fictional approved assistant', data_class='public', decision_impact='informational',
        tool_status='approved', external_tool=True, human_review=True,
        fully_automated=False, public_facing=True, prohibited_use=False)
    return {**result, **changes}

def review(**changes):
    result = dict(reviewer='Taylor Brooks', status='Approved with conditions',
        notes='Limited to public information and staff verification.',
        conditions='Staff verify facts and approve every final advisory.', next_review='2026-12-30')
    return {**result, **changes}

class IntakeTests(unittest.TestCase):
    def test_heat_advisory_is_pending_moderate(self):
        result = evaluate_proposal(proposal())
        self.assertEqual(result.decision.tier, 'moderate')
        self.assertEqual(result.decision.rule_ids, ('R07',))
        self.assertEqual(result.status, 'Pending review')
        self.assertEqual(result.route, 'Security and data governance')

    def test_restricted_unapproved_tool_is_blocked(self):
        result = evaluate_proposal(proposal(data_class='restricted', tool_status='unapproved', public_facing=False))
        self.assertEqual(result.decision.tier, 'unacceptable')
        self.assertEqual(result.decision.rule_ids, ('R02', 'R04'))
        self.assertEqual(result.status, 'Blocked')

    def test_low_and_high_routes(self):
        self.assertEqual(evaluate_proposal(proposal(public_facing=False)).route, 'Supervisor')
        self.assertEqual(evaluate_proposal(proposal(data_class='restricted')).route,
                         'Governance committee with privacy and legal review')

    def test_blank_metadata_rejected(self):
        for key in ('title', 'owner', 'department', 'purpose', 'tool'):
            with self.subTest(field=key), self.assertRaises(ValueError):
                evaluate_proposal(proposal(**{key: '  '}))

    def test_non_text_metadata_rejected(self):
        with self.assertRaises(ValueError): evaluate_proposal(proposal(owner=12))

    def test_title_length_boundary(self):
        self.assertEqual(len(evaluate_proposal(proposal(title='x'*200)).title), 200)
        with self.assertRaises(ValueError): evaluate_proposal(proposal(title='x'*201))

    def test_input_not_mutated_and_spaces_trimmed(self):
        case = proposal(owner='  Jordan Lee  ')
        before = dict(case)
        self.assertEqual(evaluate_proposal(case).owner, 'Jordan Lee')
        self.assertEqual(case, before)

    def test_non_object_intake_rejected(self):
        with self.assertRaises(ValueError): evaluate_proposal([])

class ReviewTests(unittest.TestCase):
    def run_review(self, tier='moderate', **changes):
        return validate_review(tier, 'Jordan Lee', review(**changes), today=TODAY)

    def test_valid_conditional_approval(self):
        result = self.run_review()
        self.assertEqual(result.status, 'Approved with conditions')
        self.assertEqual(result.next_review, '2026-12-30')

    def test_blocked_approval_rejected(self):
        with self.assertRaisesRegex(ValueError, 'blocks approval'):
            self.run_review(tier='unacceptable')

    def test_blocked_case_can_request_information(self):
        result = self.run_review(tier='unacceptable', status='Needs information')
        self.assertEqual(result.status, 'Needs information')

    def test_owner_cannot_approve_under_same_entered_name(self):
        with self.assertRaises(ValueError): self.run_review(reviewer='  JORDAN LEE  ')

    def test_conditions_and_date_required(self):
        for change in [{'conditions':''}, {'next_review':''}]:
            with self.subTest(change=change), self.assertRaises(ValueError): self.run_review(**change)

    def test_date_boundary_today_rejected_tomorrow_accepted(self):
        with self.assertRaises(ValueError): self.run_review(next_review='2026-10-01')
        self.assertEqual(self.run_review(next_review='2026-10-02').next_review, '2026-10-02')

    def test_invalid_date_rejected(self):
        for value in ['2026-02-30','tomorrow','20261230']:
            with self.subTest(value=value), self.assertRaises(ValueError): self.run_review(next_review=value)

    def test_unknown_status_and_tier_rejected(self):
        with self.assertRaises(ValueError): self.run_review(status='Active')
        with self.assertRaises(ValueError): self.run_review(tier='unknown')

    def test_rationale_and_reviewer_required(self):
        for change in [{'reviewer':''}, {'notes':''}]:
            with self.subTest(change=change), self.assertRaises(ValueError): self.run_review(**change)

    def test_optional_fields_must_be_text(self):
        for change in [{'conditions':[]}, {'next_review':123}]:
            with self.subTest(change=change), self.assertRaises(ValueError): self.run_review(**change)
