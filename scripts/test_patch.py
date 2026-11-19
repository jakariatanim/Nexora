import os
import re

source_path = "frontend/src/app/myadminerapanel/page.tsx"
with open(source_path, "r", encoding="utf-8") as f:
    code = f.read()

# Let's inspect sections in code to make sure replacements are exact
print("Original code length:", len(code))
