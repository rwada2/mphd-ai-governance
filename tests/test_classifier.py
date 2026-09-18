import json
from pathlib import Path
import unittest
from src.classifier import classify, VERSION

CASES = json.loads((Path(__file__).parents[1] / 'data/scenarios.json').read_text())

class ClassifierTests(unittest.TestCase):
    def test_missing_field_is_held(self):
        case = dict(CASES[0]); del case['data_class']
        with self.assertRaises(ValueError): classify(case)
    def test_unknown_data_class_is_held(self):
        with self.assertRaises(ValueError): classify({**CASES[0], 'data_class':'unknown'})
    def test_boolean_strings_are_rejected(self):
        with self.assertRaises(ValueError): classify({**CASES[0], 'human_review':'false'})
    def test_contradictory_automation_is_held(self):
        with self.assertRaises(ValueError): classify({**CASES[0], 'fully_automated':True})
    def test_prohibited_use_overrides_low(self):
        d = classify({**CASES[0], 'prohibited_use':True})
        self.assertEqual(d.tier, 'unacceptable'); self.assertIn('R01',d.rule_ids)
    def test_highest_tier_wins(self):
        self.assertEqual(classify(CASES[7]).tier,'unacceptable')
    def test_all_matching_rules_are_retained(self):
        self.assertEqual(set(classify(CASES[6]).rule_ids), {'R03','R04','R05','R06','R07'})
    def test_decision_reproducible_and_versioned(self):
        a,b = classify(CASES[4]),classify(CASES[4])
        self.assertEqual(a,b); self.assertEqual(a.rule_version,VERSION)
    def test_input_not_mutated(self):
        case = dict(CASES[0]); before = dict(case); classify(case)
        self.assertEqual(case,before)

def scenario_test(case):
    def test(self): self.assertEqual(classify(case).tier,case['expected'])
    return test
for case in CASES:
    setattr(ClassifierTests, 'test_'+case['id'],scenario_test(case))

if __name__ == '__main__': unittest.main()
