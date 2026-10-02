"""Pure intake and review rules extracted from the Week 4 prototype.

Only fictional metadata. Entered names do not establish authenticated identity.
Persistence and the browser adapter are outside this module's unit boundary.
"""
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import date
from src.classifier import Decision, classify

ROUTES = {
    'low': 'Supervisor',
    'moderate': 'Security and data governance',
    'high': 'Governance committee with privacy and legal review',
    'unacceptable': 'Blocked pending policy reconsideration',
}
STATUSES = {'Pending review', 'Under review', 'Needs information',
            'Approved with conditions', 'Declined', 'Blocked'}

def text_field(data, key, limit=200, required=True):
    value = data.get(key, '')
    if not isinstance(value, str):
        raise ValueError(f'{key} must be text')
    value = value.strip()
    if required and not value:
        raise ValueError(f'{key} is required')
    if len(value) > limit:
        raise ValueError(f'{key} exceeds {limit} characters')
    return value

@dataclass(frozen=True)
class IntakeResult:
    title: str
    owner: str
    decision: Decision
    route: str
    status: str

def evaluate_proposal(data):
    if not isinstance(data, Mapping):
        raise ValueError('A proposal object is required')
    values = {key: text_field(data, key, 2000 if key == 'purpose' else 200)
              for key in ('title', 'owner', 'department', 'purpose', 'tool')}
    decision = classify(data)
    status = 'Blocked' if decision.tier == 'unacceptable' else 'Pending review'
    return IntakeResult(values['title'], values['owner'], decision,
                        ROUTES[decision.tier], status)

@dataclass(frozen=True)
class ReviewResult:
    reviewer: str
    status: str
    notes: str
    conditions: str
    next_review: str

def validate_review(tier, owner, data, *, today=None):
    if tier not in ROUTES:
        raise ValueError('Unknown classification tier')
    if not isinstance(owner, str) or not owner.strip():
        raise ValueError('A proposal owner is required')
    if not isinstance(data, Mapping):
        raise ValueError('A review object is required')
    reviewer = text_field(data, 'reviewer')
    status = text_field(data, 'status')
    notes = text_field(data, 'notes', 2000)
    conditions = text_field(data, 'conditions', 2000, required=False)
    next_review = text_field(data, 'next_review', 10, required=False)
    if status not in STATUSES:
        raise ValueError('Unknown review status')
    if next_review:
        try:
            parsed = date.fromisoformat(next_review)
        except ValueError:
            raise ValueError('Use a valid ISO review date') from None
        if parsed.isoformat() != next_review:
            raise ValueError('Use YYYY-MM-DD for the review date')
        if parsed <= (today if today is not None else date.today()):
            raise ValueError('The next review date must be in the future')
    if status == 'Approved with conditions' and (not conditions or not next_review):
        raise ValueError('Conditional approval requires conditions and a future date')
    if tier == 'unacceptable' and status not in {'Blocked', 'Needs information', 'Declined'}:
        raise ValueError('The illustrative policy blocks approval')
    if status == 'Approved with conditions' and reviewer.casefold() == owner.strip().casefold():
        raise ValueError('Reviewer must differ from owner; entered names are not authentication')
    return ReviewResult(reviewer, status, notes, conditions, next_review)
