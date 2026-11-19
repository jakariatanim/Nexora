const fs = require('fs');
const path = require('path');

const files = [
  'samsung-official.svg',
  'oppo-official.svg',
  'vivo-official.svg',
  'sony-official.svg',
  'realme-official.svg',
  'anker-official.svg',
  'apple.svg',
  'xiaomi.svg',
  'oneplus.svg',
  'google.svg'
];

files.forEach(f => {
  const p = path.join('frontend', 'public', 'brands', f);
  if (!fs.existsSync(p)) {
    console.log(f, 'DOES NOT EXIST');
    return;
  }
  const c = fs.readFileSync(p, 'utf8');
  const vbMatch = c.match(/viewBox=["']([^"']+)["']/i);
  const wMatch = c.match(/width=["']([^"']+)["']/i);
  const hMatch = c.match(/height=["']([^"']+)["']/i);
  console.log(`File: ${f}`);
  console.log(`  viewBox: ${vbMatch ? vbMatch[1] : 'NONE'}`);
  console.log(`  w: ${wMatch ? wMatch[1] : 'NONE'}, h: ${hMatch ? hMatch[1] : 'NONE'}`);
});
