# Introduction to GitHub

<img src="https://octodex.github.com/images/Professortocat_v2.png" align="right" height="200px" />

Hey @joyroy0521!

Mona here. I'm done preparing your exercise. Hope you enjoy! 💚

Remember, it's self-paced so feel free to take a break! ☕️

[![](https://img.shields.io/badge/Go%20to%20Exercise-%E2%86%92-1f883d?style=for-the-badge&logo=github&labelColor=197935)](https://github.com/joyroy0521/skills-introduction-to-github/issues/1)

## Regulatory Dashboard

This repository also includes a simple dashboard that analyses an organisation's
profile (geography, industry, products and suppliers) and lists relevant
regulatory categories and potential risks.

Run it with:

```bash
python regulatory_dashboard.py sample_profile.json
```

Modify `sample_profile.json` with your own data to evaluate different
scenarios.

## PFAS Reporting MVP

The repository now contains a reference implementation of a PFAS reporting
workflow inspired by the business requirements document in this exercise.
It ingests supplier declarations from a CSV file and produces a JSON report
aligned to EPA TSCA §8(a)(7) field names.

Run it with:

```bash
python pfas_reporting.py sample_suppliers.csv report.json --pfas-dict pfas_list.txt
```

The generated `report.json` summarises supplier responses and lists mapped
declarations ready for further processing or submission.

## PFAS Reporting Frontend

This repository includes a minimal Flask web interface for generating reports from the browser.

Run it with:

```bash
python -m pip install flask
python pfas_frontend.py
```

Open <http://127.0.0.1:5000> and upload the supplier CSV and optional PFAS dictionary to receive the JSON report.

---

&copy; 2025 GitHub &bull; [Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/code_of_conduct.md) &bull; [MIT License](https://gh.io/mit)

