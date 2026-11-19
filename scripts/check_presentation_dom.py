import re
from html.parser import HTMLParser

with open('NEXORA_INTERACTIVE_PRESENTATION.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract all IDs in HTML
class IDParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
    def handle_starttag(self, tag, attrs):
        for k, v in attrs:
            if k == 'id':
                self.ids.add(v)

parser = IDParser()
parser.feed(content)

# Extract getElementById references in JS
js_ids = set(re.findall(r"getElementById\(['\"]([^'\"]+)['\"]\)", content))

missing = [i for i in js_ids if i not in parser.ids]
print(f"Total IDs in DOM: {len(parser.ids)}")
print(f"Total IDs referenced in JS: {len(js_ids)}")
print(f"Missing IDs: {missing}")

# Check onclick functions
onclicks = re.findall(r'onclick="([^"(]+)\(', content)
print(f"Total onclick handlers: {len(onclicks)}")
unique_onclicks = set(onclicks)
print("Unique onclick functions:", sorted(list(unique_onclicks)))
