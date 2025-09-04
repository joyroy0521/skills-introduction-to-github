"""Simple dashboard for regulatory analysis.

This script loads an organization profile from JSON and prints
regulatory categories and risks based on geography, industry,
products, and suppliers.
"""
import json
import sys
from collections import defaultdict

# Mapping of profile aspects to regulatory categories and risks
GEOGRAPHY_RULES = {
    "USA": {"categories": ["OSHA", "EPA"], "risks": ["labor", "environment"]},
    "EU": {"categories": ["GDPR", "REACH"], "risks": ["privacy", "chemical"]},
    "Asia": {"categories": ["APAC Trade"], "risks": ["import/export"]},
}

INDUSTRY_RULES = {
    "finance": {"categories": ["SOX"], "risks": ["fraud"]},
    "manufacturing": {"categories": ["ISO9001"], "risks": ["quality"]},
}

PRODUCT_RULES = {
    "electronics": {"categories": ["WEEE"], "risks": ["e-waste"]},
    "food": {"categories": ["FDA"], "risks": ["contamination"]},
}

SUPPLIER_RULES = {
    "chemical": {"categories": ["Hazmat"], "risks": ["hazardous materials"]},
    "software": {"categories": ["Licensing"], "risks": ["intellectual property"]},
}

RULESETS = {
    "geography": GEOGRAPHY_RULES,
    "industry": INDUSTRY_RULES,
    "products": PRODUCT_RULES,
    "suppliers": SUPPLIER_RULES,
}

def analyze_profile(profile: dict) -> dict:
    """Return regulatory categories and risks for a profile.

    The result is a dict with two keys, ``categories`` and ``risks``,
    each containing a sorted list of unique values.
    """
    categories = set()
    risks = set()

    for key, rules in RULESETS.items():
        values = profile.get(key, [])
        for value in values:
            info = rules.get(value, {})
            categories.update(info.get("categories", []))
            risks.update(info.get("risks", []))

    return {
        "categories": sorted(categories),
        "risks": sorted(risks),
    }

def main(path: str) -> None:
    with open(path, "r", encoding="utf-8") as f:
        profile = json.load(f)

    result = analyze_profile(profile)
    print("Regulatory categories needed:")
    for cat in result["categories"]:
        print(f" - {cat}")

    print("\nPotential regulatory risks:")
    for risk in result["risks"]:
        print(f" - {risk}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python regulatory_dashboard.py <profile.json>")
        sys.exit(1)
    main(sys.argv[1])
