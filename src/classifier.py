"""Explicit illustrative MPHD policy rules; not legal advice or a production gate."""
from dataclasses import dataclass

VERSION = "MPHD-0.1"
TIERS = {"low": 0, "moderate": 1, "high": 2, "unacceptable": 3}
REQUIRED = {
    "data_class": {"public", "internal", "confidential", "restricted"},
    "decision_impact": {"informational", "consequential", "eligibility"},
    "tool_status": {"approved", "unapproved"},
}
BOOL_FIELDS = ("external_tool", "human_review", "fully_automated", "public_facing", "prohibited_use")

@dataclass(frozen=True)
class Decision:
    tier: str
    rule_ids: tuple[str, ...]
    rule_version: str = VERSION

def classify(case):
    for key, choices in REQUIRED.items():
        if case.get(key) not in choices:
            raise ValueError(f"Missing or invalid field: {key}")
    for key in BOOL_FIELDS:
        if type(case.get(key)) is not bool:
            raise ValueError(f"Missing or invalid boolean: {key}")
    if case["fully_automated"] and case["human_review"]:
        raise ValueError("Contradictory automation and review declarations")
    matches = []
    def rule(id_, tier, condition):
        if condition:
            matches.append((id_, tier))
    rule("R01", "unacceptable", case["prohibited_use"])
    rule("R02", "unacceptable", case["external_tool"] and case["tool_status"] == "unapproved")
    rule("R03", "unacceptable", case["fully_automated"] and case["decision_impact"] == "eligibility")
    rule("R04", "high", case["data_class"] == "restricted")
    rule("R05", "high", case["decision_impact"] in {"consequential", "eligibility"})
    rule("R06", "high", not case["human_review"])
    rule("R07", "moderate", case["data_class"] == "confidential" or case["public_facing"])
    if not matches:
        matches = [("R08", "low")]
    tier = max((tier for _, tier in matches), key=TIERS.__getitem__)
    return Decision(tier, tuple(id_ for id_, _ in matches))
