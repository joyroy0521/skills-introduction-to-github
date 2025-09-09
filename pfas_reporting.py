"""PFAS reporting system for SMEs.

This module implements a minimal portion of the PFAS Reporting MVP
outlined in the business requirements document (BRD).  It supports
loading supplier declarations from a CSV file, matching entries against
an internal PFAS substance dictionary, and generating a simple report
pack that mirrors fields required for EPA TSCA §8(a)(7) submissions.

The intent is to serve as a reference implementation for a more
comprehensive system that would include supplier outreach workflows,
audit trails, evidence management, and Microsoft integration.
"""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Dict, Any

# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class SupplierDeclaration:
    """Supplier-provided information for an article or substance.

    This structure roughly follows the fields in the Streamlined Form for
    article importers (Appendix A.2).
    """

    company_name: str
    contact_name: str
    email: str
    article_description: str
    pfas_presence: str  # Yes / No / Unknown
    kra_basis: str
    evidence: str | None = None
    cbi_claim: bool = False

    @classmethod
    def from_row(cls, row: Dict[str, str]) -> "SupplierDeclaration":
        """Create a declaration from a CSV row."""
        return cls(
            company_name=row.get("Company Name", "").strip(),
            contact_name=row.get("Contact Name", "").strip(),
            email=row.get("Email Address", "").strip(),
            article_description=row.get("Article Description", "").strip(),
            pfas_presence=row.get("PFAS Presence", "Unknown").strip(),
            kra_basis=row.get("Known or Reasonably Ascertainable Basis", "").strip(),
            evidence=row.get("Evidence", "").strip() or None,
            cbi_claim=row.get("CBI Claim", "").strip().lower() in {"true", "yes", "1"},
        )


# ---------------------------------------------------------------------------
# PFAS dictionary and matching
# ---------------------------------------------------------------------------

class PFASDictionary:
    """Simple in-memory dictionary of PFAS substances.

    In a production system this could be backed by a SharePoint list or a
    database table.  For the MVP we load substances from a plain-text file
    where each line contains a CAS registry number or substance name.
    """

    def __init__(self, entries: Iterable[str]):
        self.entries = {e.strip().lower() for e in entries if e.strip()}

    @classmethod
    def from_file(cls, path: Path) -> "PFASDictionary":
        with open(path, "r", encoding="utf-8") as f:
            return cls(f.readlines())

    def contains(self, substance: str) -> bool:
        return substance.lower().strip() in self.entries


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

class ReportGenerator:
    """Generate report packs for EPA submission.

    The generator produces a JSON document that maps internal fields to
    the EPA field names outlined in Appendix B.
    """

    def __init__(self, declarations: Iterable[SupplierDeclaration]):
        self.declarations = list(declarations)

    def response_rate(self) -> float:
        """Return the fraction of suppliers that provided a PFAS answer."""
        answered = sum(1 for d in self.declarations if d.pfas_presence)
        total = len(self.declarations) or 1
        return answered / total

    def generate(self) -> Dict[str, Any]:
        mapped: List[Dict[str, Any]] = []
        for d in self.declarations:
            mapped.append(
                {
                    "Reporting Entity Name": d.company_name,
                    "Contact Name": d.contact_name,
                    "Email": d.email,
                    "Article Description": d.article_description,
                    "PFAS Presence": d.pfas_presence,
                    "Known or Reasonably Ascertainable Basis": d.kra_basis,
                    "Evidence": d.evidence,
                    "CBI Claim": d.cbi_claim,
                }
            )

        return {
            "summary": {
                "supplier_count": len(self.declarations),
                "response_rate": self.response_rate(),
            },
            "declarations": mapped,
        }

    def write(self, path: Path) -> None:
        data = self.generate()
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)


# ---------------------------------------------------------------------------
# CSV ingestion helper
# ---------------------------------------------------------------------------


def load_declarations(csv_path: Path) -> List[SupplierDeclaration]:
    """Read declarations from a CSV file."""
    with open(csv_path, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return [SupplierDeclaration.from_row(row) for row in reader]


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------


def main(csv_path: str, report_path: str, dict_path: str | None = None) -> None:
    declarations = load_declarations(Path(csv_path))

    if dict_path:
        dictionary = PFASDictionary.from_file(Path(dict_path))
        for decl in declarations:
            if decl.pfas_presence.lower() == "unknown":
                # Very naive matching: check if the description contains any
                # PFAS substance name from the dictionary.
                if any(name in decl.article_description.lower() for name in dictionary.entries):
                    decl.pfas_presence = "Yes"

    report = ReportGenerator(declarations)
    report.write(Path(report_path))
    print(f"Generated report with {len(declarations)} suppliers -> {report_path}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="PFAS Reporting MVP")
    parser.add_argument("csv", help="Path to supplier declaration CSV")
    parser.add_argument("output", help="Path to JSON report to create")
    parser.add_argument(
        "--pfas-dict",
        dest="pfas_dict",
        help="Optional path to PFAS substance dictionary (one entry per line)",
    )
    args = parser.parse_args()

    main(args.csv, args.output, args.pfas_dict)
