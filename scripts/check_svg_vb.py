import glob, os, re

for f in sorted(glob.glob('frontend/public/brands/*.svg')):
    with open(f, encoding='utf-8') as fp:
        c = fp.read()
    vb = re.search(r'viewBox="([^"]*)"', c)
    print(f"{os.path.basename(f):20s} | current: {vb.group(1) if vb else 'None'}")
