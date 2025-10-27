import os
from bs4 import BeautifulSoup

def audit_html(path):
    issues = []
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            soup = BeautifulSoup(f, 'html.parser')
            # images without alt
            for img in soup.find_all('img'):
                if not img.has_attr('alt') or not img['alt'].strip():
                    issues.append({'file': path, 'issue': 'img-missing-alt', 'element': str(img)[:200]})
            # inputs/buttons without labels/aria
            for el in soup.find_all(['button','input','a']):
                text = el.get_text(strip=True) or ''
                has_label = el.has_attr('aria-label') or el.has_attr('aria-labelledby') or bool(text)
                if not has_label:
                    issues.append({'file': path, 'issue': 'control-missing-label', 'element': str(el)[:200]})
            # headings order simple check
            headings = [h.name for h in soup.find_all(['h1','h2','h3','h4','h5','h6'])]
            last = 0
            for h in headings:
                level = int(h[1])
                if level - last > 1:
                    issues.append({'file': path, 'issue': 'heading-skip', 'headings': headings})
                    break
                last = level
    except Exception:
        pass
    return issues

def run_a11y_audit(source_folder):
    all_issues = []
    for root, _, files in os.walk(source_folder):
        for f in files:
            if f.endswith('.html'):
                path = os.path.join(root, f)
                all_issues.extend(audit_html(path))
    return all_issues
