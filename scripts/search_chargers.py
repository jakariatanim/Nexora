import sys
sys.path.append('.')
from scripts.test_startech_search import search_startech

for term in ['Samsung 45W', 'Samsung 25W', 'Xiaomi 120W', 'Xiaomi 67W', 'Google 30W', 'Google 45W', 'Anker 100W', 'Anker GaN']:
    print(f'=== {term} ===')
    for t, u in search_startech(term)[:2]:
        print(f'  {t} -> {u}')
