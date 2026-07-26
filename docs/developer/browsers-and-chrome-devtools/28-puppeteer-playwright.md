---
title: Puppeteer & Playwright
description: "Puppeteer và Playwright — headless browser automation libraries: so sánh, setup, patterns và best practices cho testing và scraping"
tags: [puppeteer, playwright, headless-browser, browser-automation, e2e-testing]
category: developer
updated: 2026-07-26
order: 28
---

# Puppeteer & Playwright

Browser automation — Puppeteer (Google) và Playwright (Microsoft).

---

## So sánh

| Tính năng | Puppeteer | Playwright |
|-----------|-----------|-----------|
| Browser | Chrome/Chromium | **Chrome, Firefox, WebKit** |
| Language | Node.js | **Node.js, Python, Java, .NET** |
| Auto-wait | Manual | **Built-in** |
| Network intercept | `setRequestInterception` | **`route()` abort/fulfill/mock** |
| Debugging | DevTools | **Playwright Inspector** |
| Test framework | Basic | **@playwright/test** |

---

## When to Use

| Use Case | Chọn | Lý do |
|----------|------|-------|
| Chrome-only scraping | Puppeteer | Lightweight |
| Multi-browser testing | Playwright | Firefox + WebKit |
| Multi-language | Playwright | Python/Java/.NET |
| Quick script | Puppeteer | Less boilerplate |
| E2E test suite | Playwright | Test runner built-in |

---

## Setup

```bash
npm install puppeteer          # Puppeteer + Chromium download
npm install puppeteer-core     # Puppeteer, use existing Chrome
npm init playwright@latest     # Playwright setup + browsers
```

---

## Basic Usage

```javascript
// Puppeteer
const puppeteer = require('puppeteer');
const browser = await puppeteer.launch();
const page = await browser.newPage();
await page.goto('https://example.com');
await page.screenshot({ path: 'shot.png' });
await browser.close();

// Playwright
const { chromium } = require('playwright');
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto('https://example.com');
await page.screenshot({ path: 'shot.png' });
await browser.close();
```

---

## Operations Reference

| Action | Puppeteer | Playwright |
|--------|-----------|------------|
| Navigate | `goto(url, {waitUntil:'networkidle2'})` | `goto(url, {waitUntil:'networkidle'})` |
| Click | `click('#btn')` | `click('#btn')` / `locator('#btn').click()` |
| Type | `type('#input', text, {delay:100})` | `fill('#input', text)` |
| Wait | `waitForSelector('.sel')` | `locator('.sel').waitFor()` |
| Screenshot | `screenshot({fullPage:true})` | `screenshot({fullPage:true})` |
| PDF | `pdf({format:'A4'})` | `pdf({format:'A4'})` |
| Block images | `setRequestInterception` + abort | `route('**/*.{png,jpg}', r => r.abort())` |
| Mock API | `request.continue({body:...})` | `route('**/api/**', r => r.fulfill({body:...}))` |

---

## Playwright Auto-Wait

```javascript
// Playwright tự động wait visible + enabled trước khi action
await page.click('#btn');     // auto-wait
await page.fill('#input', 'x'); // auto-wait visible
await page.locator('text=Submit').click();
```

---

## Playwright Test

```javascript
const { test, expect } = require('@playwright/test');

test('homepage has title', async ({ page }) => {
  await page.goto('https://example.com');
  await expect(page).toHaveTitle(/Example/);
});
```

---

## Common Patterns

```javascript
// Auth — save/load cookies
const cookies = await page.cookies();
fs.writeFileSync('cookies.json', JSON.stringify(cookies));
await page.setCookie(...JSON.parse(fs.readFileSync('cookies.json')));

// Infinite scroll
await page.evaluate(async () => {
  await new Promise(r => {
    let total = 0;
    const t = setInterval(() => {
      window.scrollBy(0, 100); total += 100;
      if (total >= document.body.scrollHeight) { clearInterval(t); r(); }
    }, 100);
  });
});

// File upload (Playwright)
const chooser = page.waitForEvent('filechooser');
await page.click('#upload');
(await chooser).setFiles('file.pdf');
```

---

## Headless vs Headed

```javascript
// Headless (default, no UI)
await puppeteer.launch({ headless: true });
// Headed (visible, for debugging)
await puppeteer.launch({ headless: false });
await chromium.launch({ headless: false }); // Playwright
```

---

## Tips

| Tip | Mô tả |
|-----|-------|
| Headed for debugging | `headless: false` |
| Set viewport | Stable screenshot size |
| Auto-wait (Playwright) | Avoid flaky tests |
| Mock API | Faster, reliable tests |
| Reuse browser instance | Launch once, test many |
| Handle dialogs | `page.on('dialog')` |

---

Xem thêm: [CDP](27-cdp.md) | [Browser Automation](29-browser-automation.md) | [Reverse Engineering](30-reverse-engineering.md)