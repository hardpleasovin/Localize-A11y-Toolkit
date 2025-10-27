import os, re, json
import regex as re2
from collections import defaultdict

I18N_PATTERN = re.compile(r"t\(['\"](?P<key>[\w\.\-:]+)['\"]\)|__\(['\"](?P<key2>[\w\.\-:]+)['\"]\)")

def extract_keys_from_text(text):
    keys = set()
    for m in I18N_PATTERN.finditer(text):
        k = m.group('key') or m.group('key2')
        if k:
            keys.add(k)
    # also look for data-i18n="key" attributes
    for m in re2.finditer(r'data-i18n\s*=\s*["\']([^"\']+)["\']', text):
        keys.add(m.group(1))
    return keys

def load_locales(locales_folder):
    locales = {}
    for fname in os.listdir(locales_folder):
        if fname.endswith('.json'):
            path = os.path.join(locales_folder, fname)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    locales[fname] = json.load(f)
            except Exception:
                locales[fname] = {}
    return locales

def nested_get(d, key_path):
    parts = key_path.split('.')
    v = d
    for p in parts:
        if isinstance(v, dict) and p in v:
            v = v[p]
        else:
            return None
    return v

def scan_i18n(source_folder, locales_folder):
    keys = set()
    for root, _, files in os.walk(source_folder):
        for f in files:
            if f.endswith(('.html','.js','.jsx','.ts','.tsx')):
                path = os.path.join(root, f)
                try:
                    with open(path, 'r', encoding='utf-8', errors='ignore') as fh:
                        txt = fh.read()
                        keys.update(extract_keys_from_text(txt))
                except Exception:
                    continue
    locales = load_locales(locales_folder)
    missing = defaultdict(list)
    for key in sorted(keys):
        for locale_name, data in locales.items():
            if nested_get(data, key) is None:
                missing[locale_name].append(key)
    return {'found_keys': sorted(list(keys)), 'missing': missing}
