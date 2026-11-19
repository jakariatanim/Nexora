const fs = require('fs');

['oppo-official.svg', 'vivo-official.svg', 'sony-official.svg', 'realme-official.svg', 'anker-official.svg'].forEach(f => {
  const c = fs.readFileSync('frontend/public/brands/' + f, 'utf8');
  console.log('===', f, '===');
  // Check paths and fills
  const paths = c.match(/<path[^>]+>/g) || [];
  console.log(`Path count: ${paths.length}`);
  paths.slice(0, 3).forEach(p => console.log(' ', p.substring(0, 150)));
});
