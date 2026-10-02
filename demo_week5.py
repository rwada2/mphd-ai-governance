"""Reproduce Week 5 evidence using synthetic data and pure modules."""
import json
from dataclasses import asdict
from datetime import date
from src.workflow import evaluate_proposal, validate_review

def main():
    case = dict(title='Drafting public heat advisories', owner='Jordan Lee',
        department='Communications', purpose='Draft from public sources with staff verification.',
        tool='Fictional approved assistant', data_class='public', decision_impact='informational',
        tool_status='approved', external_tool=True, human_review=True,
        fully_automated=False, public_facing=True, prohibited_use=False)
    print('SYNTHETIC HEAT ADVISORY')
    print(json.dumps(asdict(evaluate_proposal(case)), indent=2))
    blocked = {**case, 'data_class':'restricted', 'tool_status':'unapproved', 'public_facing':False}
    result = evaluate_proposal(blocked)
    print('\nRESTRICTED INFORMATION IN UNAPPROVED EXTERNAL TOOL')
    print('tier:',result.decision.tier,'| rules:',', '.join(result.decision.rule_ids),'| status:',result.status)
    review = dict(reviewer='Taylor Brooks', status='Approved with conditions',
        notes='Limited to public information and staff verification.',
        conditions='Staff approve every final advisory.', next_review='2026-12-30')
    print('\nREVIEW CHECKS | fixed reference date 2026-10-01')
    print('moderate:',validate_review('moderate',case['owner'],review,today=date(2026,10,1)).status)
    try:
        validate_review('unacceptable',case['owner'],review,today=date(2026,10,1))
    except ValueError as error:
        print('unacceptable:',error)
    print('\nMALFORMED INPUT CHECK')
    try:
        evaluate_proposal({**case, 'data_class':[]})
    except ValueError as error:
        print(type(error).__name__+': '+str(error))

if __name__ == '__main__':
    main()
