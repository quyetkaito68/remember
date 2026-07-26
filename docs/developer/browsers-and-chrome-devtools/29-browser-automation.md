---
title: Browser Automation
description: "Browser Automation tổng hợp — patterns, best practices, anti-detection, parallel execution, error handling cho automation scripts"
tags: [browser-automation, automation-patterns, anti-detection, parallel-execution, error-handling]
category: developer
updated: 2026-07-26
order: 29
---

# Browser Automation

Điều khiển browser bằng code: testing, scraping, data entry, monitoring.

---

## When to Use

| Dùng | Không dùng |
|------|-----------|
| E2E testing | Unit testing |
| Web scraping (complex) | Simple API calls |
| Form filling | Direct API integration |
| Screenshot/PDF | Static content |

---

## Architecture

```text
┌─────────────────────────────────────────┐
│  Application  (test/scraping scripts)   │
├─────────────────────────────────────────┤
│  Automation   (Puppeteer/Playwright)    │
├─────────────────────────────────────────┤
│  Protocol     (CDP / WebDriver / BiDi)  │
├─────────────────────────────────────────┤
│  Browser      (Chrome/Firefox/WebKit)   │
└─────────────────────────────────────────┘
```

---

## Patterns

### 1. Page Object Model

```javascript
class LoginPage {
  constructor(page) {
    this.usernameInput = page.locator('#username');
    this.passwordInput = page.locator('#password');
    this.submitButton = page.locator('button[type="submit"]');
  }
  async login(u, p) {
    await this.usernameInput.fill(u);
    await this.passwordInput.fill(p);
    await this.submitButton.click();
  }
}
// Usage: new LoginPage(page).login('user@test.com', 'pw');
```

### 2. Randomized Delays

```javascript
const delay = (min=500, max=2000) =>
  new Promise(r => setTimeout(r, Math.random()*(max-min)+min));
await page.click('#btn');
await delay();
```

### 3. Error Recovery

```javascript
async function safeGoto(page, url, retries=3) {
  for (let i=0; i<retries; i++) {
    try { return await page.goto(url, {waitUntil:'networkidle', timeout:30000}); }
    catch (e) { if (i===retries-1) throw e; await page.waitForTimeout(2000*(i+1)); }
  }
}
```

### 4. Data Extraction

```javascript
return await page.evaluate(() =>
  Array.from(document.querySelectorAll('.product-card')).map(c => ({
    name: c.querySelector('.name')?.textContent?.trim(),
    price: c.querySelector('.price')?.textContent?.trim(),
  }))
);
```

### 5. Pagination

```javascript
while (true) {
  allData.push(...await scrapeProducts(page));
  const next = page.locator('a.next-page');
  if (await next.isVisible()) { await next.click(); await page.waitForLoadState('networkidle'); }
  else break;
}
```

---

## Anti-Detection

```text
Detection Vectors:
  WebDriver flag ──────▶ --disable-blink-features=AutomationControlled
  Timing patterns ─────▶ Random delays, human typing speed
  Fingerprint ─────────▶ Canvas/WebGL spoof, UA rotation, proxy rotation
```

| Technique | Mô tả |
|-----------|--------|
| Random delays | Between actions, typing speed |
| UA rotation | Different browsers |
| Viewport randomization | Different screen sizes |
| Proxy rotation | Different IPs |
| WebDriver flag removal | `navigator.webdriver = false` |

```javascript
const browser = await puppeteer.launch({
  args: ['--disable-blink-features=AutomationControlled']
});
await page.evaluateOnNewDocument(() => {
  Object.defineProperty(navigator, 'webdriver', { get: () => false });
});
```

---

## Parallel Execution

```javascript
// Playwright
module.exports = { workers: 4 };

// Puppeteer
async function scrapeUrls(urls, concurrency=5) {
  const browser = await puppeteer.launch();
  const results = [];
  for (const chunk of chunkArray(urls, concurrency)) {
    results.push(...await Promise.all(chunk.map(async url => {
      const page = await browser.newPage();
      await page.goto(url);
      const data = await page.evaluate(() => document.title);
      await page.close();
      return { url, data };
    })));
  }
  await browser.close();
  return results;
}
```

---

## Error Handling

| Error | Recovery |
|-------|---------|
| Timeout | Increase timeout, retry with backoff |
| Element not found | Wait longer, check selector |
| Navigation failed | Retry |
| Dialog popup | `page.on('dialog')` |
| Crash | Restart browser, resume from checkpoint |
| Rate limited | Add delay, rotate proxy |

---

## Screenshot & PDF

```javascript
await page.screenshot({ path: 'full.png', fullPage: true });
await page.locator('.header').screenshot({ path: 'header.png' });
await page.pdf({ path: 'doc.pdf', format: 'A4', printBackground: true });
```

---

## Monitoring

```javascript
page.on('request', req => console.log(`${req.method()} ${req.url()}`));
page.on('console', msg => console.log(`[${msg.type()}] ${msg.text()}`));
page.on('pageerror', err => console.error(err.message));
```

---

## Best Practices Checklist

| # | Practice | Priority |
|---|----------|---------|
| 1 | Auto-wait (Playwright) | High |
| 2 | Page Object Model | High |
| 3 | Random delays | Medium |
| 4 | Retry with backoff | High |
| 5 | Headless for CI | Medium |
| 6 | Handle dialogs/popups | High |
| 7 | Close pages when done | Medium |
| 8 | Set viewport consistently | Medium |
| 9 | Mock API in tests | Medium |
| 10 | Log for debugging | Medium |

---

Xem thêm: [Puppeteer & Playwright](28-puppeteer-playwright.md) | [Web Scraping](31-web-scraping.md) | [Anti-bot](32-anti-bot.md)