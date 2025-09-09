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
    each containing a sorted list of unique values. The returned dict
    also contains a ``breakdown`` key with detailed information for each
    profile aspect.
    """
    categories = set()
    risks = set()
    breakdown = {key: [] for key in RULESETS}

    for key, rules in RULESETS.items():
        for value in profile.get(key, []):
            info = rules.get(value, {})
            cats = info.get("categories", [])
            rks = info.get("risks", [])
            categories.update(cats)
            risks.update(rks)
            breakdown[key].append({"value": value, "categories": cats, "risks": rks})

    return {
        "categories": sorted(categories),
        "risks": sorted(risks),
        "breakdown": breakdown,
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

    # Detailed breakdown by profile aspect for customer visibility
    print("\nBreakdown by profile aspect:")
    for aspect, entries in result["breakdown"].items():
        if not entries:
            continue
        print(f"{aspect.capitalize()}:")
        for entry in entries:
            cat_list = ", ".join(entry["categories"]) or "None"
            risk_list = ", ".join(entry["risks"]) or "None"
            print(f" - {entry['value']}: categories [{cat_list}] | risks [{risk_list}]")
        print()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python regulatory_dashboard.py <profile.json>")
        sys.exit(1)
    main(sys.argv[1])
