import re

def parse_svg_path(d):
    # Split into commands and parameters
    tokens = re.findall(r'([a-zA-Z]|[-+]?(?:\d*\.\d+|\d+))', d)
    points = []
    curr_x, curr_y = 0.0, 0.0
    start_x, start_y = 0.0, 0.0
    i = 0
    cmd = ''
    while i < len(tokens):
        t = tokens[i]
        if t.isalpha():
            cmd = t
            i += 1
            if cmd in ('z', 'Z'):
                curr_x, curr_y = start_x, start_y
            continue
        
        # Read numbers according to command
        if cmd in ('M', 'm'):
            x = float(t)
            y = float(tokens[i+1])
            i += 2
            if cmd == 'm':
                curr_x += x
                curr_y += y
            else:
                curr_x = x
                curr_y = y
            start_x, start_y = curr_x, curr_y
            points.append((curr_x, curr_y))
            cmd = 'l' if cmd == 'm' else 'L'
        elif cmd in ('L', 'l'):
            x = float(t)
            y = float(tokens[i+1])
            i += 2
            if cmd == 'l':
                curr_x += x
                curr_y += y
            else:
                curr_x = x
                curr_y = y
            points.append((curr_x, curr_y))
        elif cmd in ('H', 'h'):
            x = float(t)
            i += 1
            if cmd == 'h':
                curr_x += x
            else:
                curr_x = x
            points.append((curr_x, curr_y))
        elif cmd in ('V', 'v'):
            y = float(t)
            i += 1
            if cmd == 'v':
                curr_y += y
            else:
                curr_y = y
            points.append((curr_x, curr_y))
        elif cmd in ('C', 'c'):
            # 6 numbers: x1 y1 x2 y2 x y
            vals = [float(tokens[i+j]) for j in range(6)]
            i += 6
            if cmd == 'c':
                points.append((curr_x + vals[0], curr_y + vals[1]))
                points.append((curr_x + vals[2], curr_y + vals[3]))
                curr_x += vals[4]
                curr_y += vals[5]
            else:
                points.append((vals[0], vals[1]))
                points.append((vals[2], vals[3]))
                curr_x = vals[4]
                curr_y = vals[5]
            points.append((curr_x, curr_y))
        elif cmd in ('S', 's', 'Q', 'q'):
            # 4 numbers
            vals = [float(tokens[i+j]) for j in range(4)]
            i += 4
            if cmd in ('s', 'q'):
                points.append((curr_x + vals[0], curr_y + vals[1]))
                curr_x += vals[2]
                curr_y += vals[3]
            else:
                points.append((vals[0], vals[1]))
                curr_x = vals[2]
                curr_y = vals[3]
            points.append((curr_x, curr_y))
        elif cmd in ('A', 'a'):
            # 7 numbers: rx ry x-axis-rotation large-arc sweep x y
            vals = [float(tokens[i+j]) for j in range(7)]
            i += 7
            if cmd == 'a':
                curr_x += vals[5]
                curr_y += vals[6]
            else:
                curr_x = vals[5]
                curr_y = vals[6]
            points.append((curr_x, curr_y))
        else:
            i += 1
            
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    return min(xs), min(ys), max(xs), max(ys)

for fname in ['samsung.svg', 'sony.svg', 'oppo.svg', 'vivo.svg', 'apple.svg', 'oneplus.svg', 'xiaomi.svg']:
    with open('frontend/public/brands/' + fname, encoding='utf-8') as f:
        content = f.read()
    d = re.search(r'd="([^"]*)"', content).group(1)
    min_x, min_y, max_x, max_y = parse_svg_path(d)
    w = max_x - min_x
    h = max_y - min_y
    aspect = w / h if h > 0 else 0
    print(f"{fname:15s}: x=[{min_x:.2f}, {max_x:.2f}], y=[{min_y:.2f}, {max_y:.2f}] | w={w:.2f}, h={h:.2f} | aspect={aspect:.2f}:1")
    # Recommended tight viewBox with small 0.5 padding
    pad = 0.5
    print(f"   Recommended viewBox: '{min_x - pad:.1f} {min_y - pad:.1f} {w + 2*pad:.1f} {h + 2*pad:.1f}'")
