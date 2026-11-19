const fs = require('fs');

['oppo-official.svg', 'vivo-official.svg', 'sony-official.svg', 'realme-official.svg', 'anker-official.svg'].forEach(f => {
  const c = fs.readFileSync('frontend/public/brands/' + f, 'utf8');
  console.log('==================', f, '==================');
  // Print everything without XML comment and metadata
  const clean = c.replace(/<!--[\s\S]*?-->/g, '').replace(/<metadata>[\s\S]*?<\/metadata>/g, '').replace(/\s+/g, ' ');
  console.log(clean.substring(0, 500));
});
