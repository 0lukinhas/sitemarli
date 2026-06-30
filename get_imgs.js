const { chromium } = require('playwright-core');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('https://accurate-clone-engine.lovable.app/', { waitUntil: 'networkidle' });
  const images = await page.$$eval('img', imgs => imgs.map(img => img.src));
  
  // also check background images
  const bgImages = await page.$$eval('*', els => els.map(el => window.getComputedStyle(el).backgroundImage).filter(bg => bg !== 'none' && bg !== 'initial'));
  
  console.log("Images:", [...new Set(images)]);
  console.log("Backgrounds:", [...new Set(bgImages)]);
  await browser.close();
})();
