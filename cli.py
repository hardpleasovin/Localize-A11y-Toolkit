import click
from .i18n_scanner import scan_i18n
from .a11y_checker import run_a11y_audit
from .report_generator import generate_html_report
import json

@click.group()
def cli():
    pass

@cli.command('i18n')
@click.option('--source', required=True, help='Folder to scan for i18n keys')
@click.option('--locales', required=True, help='Folder with JSON locale files')
@click.option('--out', default='reports/i18n_report.json', help='Output JSON file')
def i18n_cmd(source, locales, out):
    report = scan_i18n(source, locales)
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    click.echo('i18n report written to ' + out)

@cli.command('a11y')
@click.option('--source', required=True, help='Folder to scan for HTML files')
@click.option('--out', default='reports/a11y_report.json', help='Output JSON file')
def a11y_cmd(source, out):
    report = run_a11y_audit(source)
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    click.echo('a11y report written to ' + out)

@cli.command('report')
@click.option('--i18n', required=True, help='Path to i18n report JSON')
@click.option('--a11y', required=True, help='Path to a11y report JSON')
@click.option('--out', default='reports/summary.html', help='Output HTML file')
def report_cmd(i18n, a11y, out):
    with open(i18n, 'r', encoding='utf-8') as f:
        i18n_report = json.load(f)
    with open(a11y, 'r', encoding='utf-8') as f:
        a11y_report = json.load(f)
    generate_html_report(i18n_report, a11y_report, out_path=out)
    click.echo('Combined HTML report written to ' + out)

if __name__ == '__main__':
    cli()
