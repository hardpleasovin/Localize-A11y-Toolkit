# Localize & A11y Toolkit

A small, practical toolkit to help developers and localization engineers find missing translations and detect common accessibility issues in HTML and React-like projects. Ready to publish on GitHub and accept sponsorships.

## Features
- CLI with three commands: `i18n`, `a11y`, `report`
- i18n scanner: extracts translation keys from HTML/JSX/JS/TS files and reports missing keys against JSON locale files
- Accessibility checker: finds missing `alt` attributes, unlabeled buttons/inputs, and simple heading-order issues
- HTML report generator (uses Jinja2) that combines i18n and a11y findings into a single report
- Sample site and locale files included for quick demo

## Install
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage
Scan for missing translations:
```bash
python -m src.cli i18n --source sample_site --locales locales --out reports/i18n_report.json
```

Run accessibility audit:
```bash
python -m src.cli a11y --source sample_site --out reports/a11y_report.json
```

Generate combined HTML report:
```bash
python -m src.cli report --i18n reports/i18n_report.json --a11y reports/a11y_report.json --out reports/summary.html
```

## Why this is useful
- Prevents missing translations from shipping to production
- Helps catch basic accessibility regressions early
- Small, dependency-light, and easy to extend for projects of any size

## Sponsor
If this tool helps your team ship inclusive, localized products, please consider supporting development via GitHub Sponsors.

## License
MIT
