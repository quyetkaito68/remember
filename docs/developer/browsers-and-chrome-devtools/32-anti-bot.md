---
title: Anti-bot, Fingerprinting & CAPTCHA
description: "Anti-bot systems, Browser Fingerprinting, CAPTCHA, Rate Limiting: cách website detect và block bots"
tags: [anti-bot, fingerprinting, captcha, rate-limiting, bot-detection, web-scraping]
category: developer
updated: 2026-07-26
order: 32
---

# Anti-bot, Fingerprinting & CAPTCHA

> Website detect bot ở 4 layers: network, browser, behavioral, challenge. Hiểu stack = bypass được.

---

## Anti-Bot Stack

```text
Layer 1: Network        → IP reputation, rate limit, TLS fingerprint (JA3)
Layer 2: Browser        → Fingerprinting, webdriver flag, headless detection
Layer 3: Behavioral     → Mouse patterns, keyboard timing, scroll behavior
Layer 4: Challenge      → CAPTCHA, JS challenge, proof of work
```

---

## Browser Fingerprinting

| Attribute | Uniqueness | Ghi chú |
|-----------|-----------|---------|
| **Canvas** | Cao | Unique rendering từ GPU/driver/OS/fonts |
| **WebGL** | Cao | GPU renderer info |
| **ClientRects** | Cao | Text rendering measurement |
| **WebRTC** | Cao | Local IP leak |
| **AudioContext** | Trung bình | Audio processing |
| **Fonts** | Trung bình | Installed fonts |
| **Battery** | Trung bình | Battery status API |
| **Plugins** | Thấp | Browser plugins |
| **Screen** | Thấp | Resolution, color depth |
| **Navigator** | Thấp | User-Agent, platform, language |
| **Timezone** | Thấp | Timezone + locale |

```javascript
// Canvas fingerprint
const canvas = document.createElement('canvas');
const ctx = canvas.getContext('2d');
ctx.textBaseline = 'top';
ctx.font = '14px Arial';
ctx.fillStyle = '#f60';
ctx.fillRect(125, 1, 62, 20);
ctx.fillStyle = '#069';
ctx.fillText('Hello', 2, 15);
const fingerprint = canvas.toDataURL('image/png');

// WebGL fingerprint
const gl = canvas.getContext('webgl');
const debugInfo = gl.getExtension('WEBGL_debug_renderer_info');
const renderer = gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL);
```

---

## Detection Techniques

### Headless Detection

| Check | Headless | Real Browser |
|-------|----------|-------------|
| `navigator.webdriver` | `true` | `undefined` |
| `window.chrome` | Missing | Present |
| `navigator.plugins` | Empty | Has plugins |
| `Notification.permission` | Different | Normal |
| User-Agent | "HeadlessChrome" | Normal |

### Behavioral Analysis

```text
Bot:                          Human:
❌ Straight mouse line        ✅ Curves with micro-jitter
❌ Instant clicks             ✅ Random delays
❌ No scroll events           ✅ Varying scroll speed
❌ Page load → instant action ✅ Page load → orient → act
```

### JavaScript Challenge

```text
Server sends JS → Browser executes → Result hash back
If code doesn't execute → Bot detected
```

---

## CAPTCHA Types

| Type | Difficulty | Bypass Difficulty |
|------|-----------|------------------|
| **reCAPTCHA v2** | Trung bình | Trung bình |
| **reCAPTCHA v3** (score-based) | Khó | Khó |
| **hCaptcha** | Trung bình | Trung bình |
| **Cloudflare Turnstile** | Thấp | Dễ |
| **Text CAPTCHA** | Thấp | Dễ |
| **Audio CAPTCHA** | Trung bình | Trung bình |

**reCAPTCHA v3 scores:** 1.0 = human, 0.5 = uncertain, 0.0 = bot. Dựa trên fingerprint + behavior + network reputation + session history.

---

## Rate Limiting

| Type | Mô tả |
|------|--------|
| **Per IP** | Limit theo IP |
| **Per User** | Limit theo account |
| **Sliding Window** | Rolling time window |
| **Token Bucket** | Allow burst, limit sustained |

```text
HTTP 429 Too Many Requests
Headers:
  Retry-After: 60
  X-RateLimit-Limit: 100
  X-RateLimit-Remaining: 0
  X-RateLimit-Reset: 1640995200
```

---

## Anti-Bot Bypass Checklist

| # | Strategy | Implementation |
|---|----------|---------------|
| 1 | Rotate IPs | Proxy pool (residential > datacenter) |
| 2 | Random delays | 2-10s between requests |
| 3 | User-Agent rotation | Multiple real browser UAs |
| 4 | Session persistence | Maintain cookies/sessions |
| 5 | Behavior simulation | Mouse movement, scrolling |
| 6 | Stealth plugin | puppeteer-extra-plugin-stealth |
| 7 | Respect robots.txt | Don't crawl blocked paths |
| 8 | Error handling | Retry with exponential backoff |

```javascript
async function scrapeWithRetry(page, url, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      await page.goto(url);
      await randomDelay(2000, 5000);
      return await extractData(page);
    } catch (error) {
      if (error.message.includes('429') || error.message.includes('403')) {
        await page.waitForTimeout(60000 * (i + 1));
        continue;
      }
      throw error;
    }
  }
}
```

---

## Stealth Tools

| Tool | Bypass |
|------|--------|
| **puppeteer-extra-plugin-stealth** | Automation flags |
| **playwright-extra** | Stealth for Playwright |
| **undetected-chromedriver** | Selenium detection |
| **cloudscraper** | Cloudflare |
| **2captcha** | CAPTCHA solving |

---

Xem thêm: [Web Scraping](31-web-scraping.md) | [Reverse Engineering](30-reverse-engineering.md) | [Browser Security](17-browser-security.md)