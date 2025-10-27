from jinja2 import Template
import os, datetime, json

TEMPLATE = '''<html><head><meta charset="utf-8"><title>Localization & A11y Report</title>
<style>body{font-family:Inter, system-ui; padding:20px} table{border-collapse:collapse;width:100%}td,th{border:1px solid #eee;padding:8px}</style>
</head><body>
<h1>Localization & Accessibility Report</h1>
<p>Generated: {{ts}}</p>

<h2>i18n - Missing Translations</h2>
{% for locale, keys in i18n_missing.items() %}
  <h3>{{locale}} ({{keys|length}} missing)</h3>
  <ul>
  {% for k in keys %}
    <li><code>{{k}}</code></li>
  {% endfor %}
  </ul>
{% endfor %}

<h2>Accessibility Issues</h2>
{% if a11y_issues|length == 0 %}
  <p>No accessibility issues found (basic checks).</p>
{% else %}
  <table><tr><th>File</th><th>Issue</th><th>Snippet</th></tr>
  {% for it in a11y_issues %}
    <tr><td>{{it.file}}</td><td>{{it.issue}}</td><td><pre>{{it.element or it.headings}}</pre></td></tr>
  {% endfor %}
  </table>
{% endif %}

</body></html>'''

def generate_html_report(i18n_report, a11y_report, out_path='reports/summary.html'):
    ts = datetime.datetime.utcnow().isoformat() + 'Z'
    tpl = Template(TEMPLATE)
    html = tpl.render(ts=ts, i18n_missing=i18n_report.get('missing', {}), a11y_issues=a11y_report)
    os.makedirs(os.path.dirname(out_path) or '.', exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print('Report generated at', out_path)
