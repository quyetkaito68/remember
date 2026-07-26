---
title: Web Scraping & Crawling
description: "Web Scraping & Crawling — techniques, tools, strategies: từ HTTP requests đơn giản đến headless browser automation"
tags: [web-scraping, web-crawling, data-extraction, scraping-tools, crawl-strategy]
category: developer
updated: 2026-07-26
order: 31
---

# Web Scraping & Crawling

> Extract data từ website. Discover và traverse links. Chọn đúng tool = đúng strategy.

---

## Scraping Strategy Decision Tree

```text
Bạn cần scrape data từ website?
│
├─ Website có API public?
│  └─ YES → Dùng API (nhanh nhất, ổn định nhất)
│
├─ Website render server-side (HTML có sẵn data)?
│  └─ YES → HTTP Request + HTML Parser (cheerio, bs4)
│
└─ Website là SPA (React/Vue/Angular)?
   └─ YES → Headless Browser (Playwright, Puppeteer)
      │
      ├─ Cần bypass anti-bot?
      │  └─ YES → Stealth plugin + proxy + delays
      │
      └─ Scale lớn (>10k pages)?
         └─ YES → Scrapy framework + crawling strategy
```

---

## Scraping vs Crawling

| Tính năng | Scraping | Crawling |
|-----------|----------|----------|
| Mục đích | Extract data | Discover pages |
| Scope | 1 hoặc nhiều pages | Toàn bộ site |
| Output | Structured data | URLs, links |
| Depth | Thường 1 level | Nhiều levels |

---

## 3 Approaches

### 1. HTTP Request (static HTML)

```javascript
const axios = require('axios');
const cheerio = require('cheerio');

async function scrape(url) {
  const { data } = await axios.get(url);
  const $ = cheerio.load(data);
  return $('.product-card').map((i, el) => ({
    name: $(el).find('.name').text().trim(),
    price: $(el).find('.price').text().trim(),
  })).get();
}
```

**Nhanh, ít resource. Không chạy JS được.**

### 2. Headless Browser (SPA / JS rendering)

```javascript
const { chromium } = require('playwright');

async function scrape(url) {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto(url, { waitUntil: 'networkidle' });
  const items = await page.evaluate(() =>
    Array.from(document.querySelectorAll('.product-card')).map(el => ({
      name: el.querySelector('.name')?.textContent?.trim(),
      price: el.querySelector('.price')?.textContent?.trim(),
    }))
  );
  await browser.close();
  return items;
}
```

**Chạy được JS. Chậm hơn, tốn resource.**

### 3. API (nếu có)

```javascript
const products = await fetch('https://api.example.com/products').then(r => r.json());
```

**Nhanh nhất. Không phải website nào cũng có.**

---

## Tool Comparison

| Tool | Language | JS Rendering | Best For |
|------|----------|-------------|----------|
| **Cheerio + Axios** | Node.js | ❌ | Static HTML, fast scraping |
| **Playwright** | Node.js/Python | ✅ | SPA, cross-browser |
| **Puppeteer** | Node.js | ✅ | Chrome-only automation |
| **Scrapy** | Python | ❌ | Large-scale crawling |
| **Beautiful Soup** | Python | ❌ | Simple parsing |
| **Selenium** | Multi | ✅ | Legacy, cross-browser |

---

## Crawler Architecture

```text
Seed URLs → URL Queue (BFS/DFS) → Fetcher → HTML Parser
                                                  │
                                    ┌─────────────┴─────────────┐
                                    ▼                           ▼
                              URL Filter (Dedup)         Data Store
```

| Strategy | Khi dùng |
|----------|---------|
| **BFS** | General crawling, level by level |
| **DFS** | Deep site exploration |
| **Best-First** | Focused crawling by importance |

---

## Data Storage

| Format | Khi dùng |
|--------|---------|
| **JSON** | Human-readable, flexible |
| **CSV** | Spreadsheet, flat data |
| **JSONL** | Streaming, append-friendly |
| **Database** | Query, scalable |

---

## Legal Checklist

| Check | Action |
|-------|--------|
| robots.txt | Respect crawl rules |
| Rate limiting | Don't overload server |
| Terms of Service | Read website ToS |
| Personal data | GDPR/CCPA compliance |
| Copyright | Respect content copyright |

---

Xem thêm: [Reverse Engineering](30-reverse-engineering.md) | [Anti-bot](32-anti-bot.md) | [Puppeteer & Playwright](28-puppeteer-playwright.md)