import os
import re
import json

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def find_html_files():
    html_files = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        for f in filenames:
            if f.endswith('.html'):
                html_files.append(os.path.join(dirpath, f))
    return html_files


def extract_data_i18n(files):
    keys = set()
    pattern = re.compile(r'data-i18n="([\w\.-]+)"')
    for path in files:
        with open(path, 'r', encoding='utf-8') as fh:
            text = fh.read()
        for m in pattern.finditer(text):
            keys.add(m.group(1))
    return keys


def extract_translations(path):
    # crude parsing: find fr: { ... } and en: { ... } and extract keys
    text = open(path, 'r', encoding='utf-8').read()
    def parse_block(name):
        m = re.search(rf"{name}\s*:\s*\{{(.*?)\n\s*\}}", text, re.S)
        if not m:
            return set()
        block = m.group(1)
        keys = set(re.findall(r'"([\w\.-]+)"\s*:', block))
        return keys
    fr_keys = parse_block('fr')
    en_keys = parse_block('en')
    return fr_keys, en_keys


def find_pdf_paths(files):
    pdfs = set()
    pattern = re.compile(r"[\w\-/]+\.pdf")
    for path in files:
        with open(path, 'r', encoding='utf-8') as fh:
            for m in pattern.finditer(fh.read()):
                pdfs.add(m.group(0))
    return pdfs


def find_links_and_assets(files):
    hrefs = set()
    srcs = set()
    href_pattern = re.compile(r'href="([^"]+)"')
    src_pattern = re.compile(r'src="([^"]+)"')
    for path in files:
        with open(path, 'r', encoding='utf-8') as fh:
            text = fh.read()
        for m in href_pattern.finditer(text):
            hrefs.add(m.group(1))
        for m in src_pattern.finditer(text):
            srcs.add(m.group(1))
    return hrefs, srcs


def main():
    html_files = find_html_files()
    print('Found HTML files:', html_files)
    data_keys = extract_data_i18n(html_files)
    print('\nData-i18n keys used in HTML (count={}):'.format(len(data_keys)))
    for k in sorted(data_keys):
        print('  ', k)

    fr_keys, en_keys = extract_translations(os.path.join(ROOT, 'assets', 'js', 'i18n.js'))
    print('\nTranslation keys (fr={}, en={})'.format(len(fr_keys), len(en_keys)))

    missing_fr = sorted([k for k in data_keys if k not in fr_keys])
    missing_en = sorted([k for k in data_keys if k not in en_keys])

    if missing_fr:
        print('\nMissing in French translations:')
        for k in missing_fr:
            print('  ', k)
    else:
        print('\nNo missing French translations for used keys.')

    if missing_en:
        print('\nMissing in English translations:')
        for k in missing_en:
            print('  ', k)
    else:
        print('\nNo missing English translations for used keys.')

    # Find unused translation keys
    unused_fr = sorted([k for k in fr_keys if k not in data_keys])
    unused_en = sorted([k for k in en_keys if k not in data_keys])
    print('\nUnused translation keys (French) count:', len(unused_fr))
    if unused_fr:
        for k in unused_fr:
            print('   FR unused:', k)
    print('\nUnused translation keys (English) count:', len(unused_en))
    if unused_en:
        for k in unused_en:
            print('   EN unused:', k)

    pdfs = find_pdf_paths(html_files)
    print('\nPDF references found:')
    for p in sorted(pdfs):
        path = os.path.join(ROOT, p.replace('/', os.sep))
        exists = os.path.exists(path)
        print('  ', p, '->', 'FOUND' if exists else 'MISSING')

        hrefs, srcs = find_links_and_assets(html_files)
        print('\nLocal links referenced (checking existence for local files):')
        for h in sorted(hrefs):
            if h.startswith('http') or h.startswith('mailto:') or h.startswith('#'):
                continue
            path = os.path.join(ROOT, h.replace('/', os.sep))
            print('  ', h, '->', 'FOUND' if os.path.exists(path) else 'MISSING')

        print('\nLocal assets referenced (src):')
        for s in sorted(srcs):
            if s.startswith('http'):
                continue
            path = os.path.join(ROOT, s.replace('/', os.sep))
            print('  ', s, '->', 'FOUND' if os.path.exists(path) else 'MISSING')

if __name__ == '__main__':
    main()
