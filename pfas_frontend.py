from __future__ import annotations

import csv
import io
from typing import List

from flask import Flask, jsonify, render_template_string, request

from pfas_reporting import PFASDictionary, ReportGenerator, SupplierDeclaration

app = Flask(__name__)

FORM_HTML = """
<!doctype html>
<title>PFAS Reporter</title>
<h1>PFAS Reporting</h1>
<form method="post" enctype="multipart/form-data">
  <label>Supplier CSV: <input type="file" name="csv" required></label><br>
  <label>PFAS Dictionary (optional): <input type="file" name="pfas_dict"></label><br>
  <input type="submit" value="Generate Report">
</form>
"""


def _load_declarations_from_csv(data: str) -> List[SupplierDeclaration]:
    reader = csv.DictReader(io.StringIO(data))
    return [SupplierDeclaration.from_row(row) for row in reader]


def _apply_dictionary(declarations: List[SupplierDeclaration], dictionary: PFASDictionary) -> None:
    for decl in declarations:
        if decl.pfas_presence.lower() == "unknown":
            if any(name in decl.article_description.lower() for name in dictionary.entries):
                decl.pfas_presence = "Yes"


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        csv_file = request.files.get("csv")
        if not csv_file:
            return "CSV file is required", 400
        csv_text = csv_file.stream.read().decode("utf-8")
        declarations = _load_declarations_from_csv(csv_text)

        dict_file = request.files.get("pfas_dict")
        if dict_file:
            dict_text = dict_file.stream.read().decode("utf-8")
            dictionary = PFASDictionary(dict_text.splitlines())
            _apply_dictionary(declarations, dictionary)

        report = ReportGenerator(declarations).generate()
        return jsonify(report)

    return render_template_string(FORM_HTML)


if __name__ == "__main__":
    app.run(debug=True)
