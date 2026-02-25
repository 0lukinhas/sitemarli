const { chromium } = require('playwright-core');

(async () => {
    try {
        const browser = await chromium.launch();
        const page = await browser.newPage();
        await page.goto('https://accurate-clone-engine.lovable.app/', { waitUntil: 'networkidle' });

        const images = await page.$$eval('img', imgs => imgs.map(img => img.src));

        let bgImages = await page.$$eval('*', els => {
            return els.map(el => {
                const bg = window.getComputedStyle(el).backgroundImage;
                if (bg && bg !== 'none' && bg !== 'initial' && bg.includes('url')) {
                    // Extract URL from 'url("...")'
                    const match = bg.match(/url\(['"]?(.*?)['"]?\)/);
                    return match ? match[1] : null;
                }
                return null;
            }).filter(url => url !== null);
        });

        console.log("--- IMAGES ---");
        [...new Set([...images, ...bgImages])].forEach(url => {
            if (url && !url.includes('data:image')) {
                console.log(url);
            }
        });

        await browser.close();
    } catch (e) {
        console.error(e);
        process.exit(1);
    }
})();
