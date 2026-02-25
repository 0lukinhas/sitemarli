const { chromium } = require('playwright-core');

(async () => {
    try {
        const browser = await chromium.launch();
        const page = await browser.newPage();
        await page.goto('https://accurate-clone-engine.lovable.app/', { waitUntil: 'networkidle' });
        
        await page.waitForTimeout(2000);
        const textContent = await page.$eval('body', el => el.innerText);
        console.log(textContent);

        await browser.close();
    } catch (e) {
        console.error(e);
        process.exit(1);
    }
})();
