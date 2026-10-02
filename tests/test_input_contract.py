"""Regression checks for malformed JSON-compatible classifier inputs."""
import json
from pathlib import Path
import unittest
from src.classifier import classify

BASE = json.loads((Path(__file__).parents[1] / 'data/scenarios.json').read_text())[0]

class InputContractTests(unittest.TestCase):
    def test_non_object_input_rejected(self):
        for value in [None, [], 'public', 1, True]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                classify(value)

    def test_collection_in_enum_rejected(self):
        for field in ['data_class', 'decision_impact', 'tool_status']:
            for value in [[], {}]:
                with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                    classify({**BASE, field: value})

    def test_integer_is_not_boolean(self):
        for field in ['external_tool', 'human_review', 'fully_automated', 'public_facing', 'prohibited_use']:
            with self.subTest(field=field), self.assertRaises(ValueError):
                classify({**BASE, field: 1})

    def test_missing_boolean_rejected(self):
        for field in ['external_tool', 'human_review', 'fully_automated', 'public_facing', 'prohibited_use']:
            case = {key:value for key,value in BASE.items() if key != field}
            with self.subTest(field=field), self.assertRaises(ValueError):
                classify(case)

    def test_unknown_extra_metadata_ignored(self):
        self.assertEqual(classify(BASE), classify({**BASE, 'display_title':'Synthetic case'}))
