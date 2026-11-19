import re

with open("scripts/build_admin_overhaul.py", "r", encoding="utf-8") as f:
    text = f.read()

start_str = "code = '''"
end_str = "\n'''\n"
s_idx = text.find(start_str) + len(start_str)
e_idx = text.rfind(end_str)
base_code = text[s_idx:e_idx]

# Replace \' with '
clean_code = base_code.replace(r"\'", "'")

# Check if there are any remaining backslashes
backslashes = [line for line in clean_code.splitlines() if "\\" in line]
print(f"Lines with backslashes after replacement: {len(backslashes)}")
for l in backslashes[:10]:
    print(repr(l))
