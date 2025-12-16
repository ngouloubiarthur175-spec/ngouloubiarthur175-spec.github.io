import re
import os
from bs4 import BeautifulSoup
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
idx = os.path.join(ROOT, 'index.html')
pro = os.path.join(ROOT, 'projects.html')

with open(idx, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'html.parser')

nav = soup.find('nav', id='site-nav')
links = [a.get_text(strip=True) for a in nav.find_all('a')]
expected_order = ['Accueil', 'Qui Je Suis ?', 'Laboratoire', 'Mes Articles', 'Éducation', 'Certification', 'Expérience Professionnelle', 'Contact']

print('Nav links found:', links)
print('Matches expected order:', links == expected_order)

# Check sections order in body: welcome -> whoiam -> labs
sections = [s.get('id') for s in soup.find_all(['header','section','footer']) if s.get('id')]
print('Section ids found in order:', sections[:6])

# Ensure projects page exists
print('projects.html exists:', os.path.exists(pro))

# Check project1 link in projects.html
if os.path.exists(pro):
    with open(pro, 'r', encoding='utf-8') as f:
        p = BeautifulSoup(f, 'html.parser')
    buttons = [b.get_text(strip=True) for b in p.find_all('button')]
    print('projects.html buttons:', buttons)

# Check pdf embedding close button style exists in CSS
css = os.path.join(ROOT, 'assets', 'css', 'main.css')
with open(css, 'r', encoding='utf-8') as f:
    txt = f.read()
print('close-pdf style present:', '.close-pdf' in txt)

# Quick check PDF path exists
pdf_path = os.path.join(ROOT, 'PROJET', 'PROJET2', 'PROJET.pdf')
print('Project PDF exists:', os.path.exists(pdf_path))
