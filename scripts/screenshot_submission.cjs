// Capture real browser renders of notebook output evidence.
// NODE_PATH must include the installed playwright package directory.
const { chromium } = require('playwright');
const { resolve } = require('node:path');
const { pathToFileURL } = require('node:url');
const { readdirSync } = require('node:fs');
(async () => {
  const browser = await chromium.launch({
    executablePath: process.env.CHROMIUM_PATH || '/usr/lib64/chromium-browser/chromium-browser',
    headless: true, args: ['--no-sandbox', '--disable-dev-shm-usage']
  });
  try {
    const page = await browser.newPage({ viewport: { width: 1600, height: 1000 }, deviceScaleFactor: 1 });
    const prefix = process.argv[2] || '';
    for (const file of readdirSync('submission/evidence').filter(f => f.endsWith('.html') && f.startsWith(prefix))) {
      await page.goto(pathToFileURL(resolve('submission/evidence', file)).href);
      await page.evaluate(() => document.fonts.ready);
      const out = resolve('submission/screenshots', file.replace('.html', '.png'));
      await page.screenshot({ path: out, fullPage: true });
      console.log(out);
    }
  } finally { await browser.close(); }
})().catch(e => { console.error(e); process.exit(1); });
