---
title: Lighthouse & Audit
description: "Lighthouse trong Chrome DevTools — audit performance, accessibility, SEO, best practices, PWA: cách chạy và interpreting kết quả"
tags: [lighthouse, audit, performance-score, accessibility, seo, best-practices, pwa]
category: developer
updated: 2026-07-26
order: 26
---

# Lighthouse & Audit

Tự động audit web page: performance, accessibility, SEO, best practices, PWA. Điểm 0-100.

---

## Chạy

```text
DevTools → Lighthouse tab → Chọn categories → Device (Mobile/Desktop) → [Analyze]
```

```bash
npm install -g lighthouse
lighthouse https://example.com --output=html --view
```

---

## Core Web Vitals

| Metric | Good | Poor | Đo lường gì |
|--------|------|------|-------------|
| **LCP** | ≤2.5s | >4.0s | Render nội dung lớn nhất |
| **FID/INP** | ≤100ms | >300ms | Respond input |
| **CLS** | ≤0.1 | >0.25 | Layout shift |
| **FCP** | ≤1.8s | >3.0s | Render content đầu tiên |
| **TBT** | ≤200ms | >600ms | Main thread blocking |

---

## Optimization Checklist

| # | Category | Action | Impact |
|---|----------|--------|--------|
| 1 | Performance | Defer non-critical JS/CSS | High |
| 2 | Performance | Convert images to WebP/AVIF | High |
| 3 | Performance | Enable Brotli/gzip | High |
| 4 | Performance | Remove unused JS | Medium |
| 5 | Performance | Set explicit image dimensions | Medium |
| 6 | Accessibility | Add form labels + alt text | High |
| 7 | Accessibility | Fix contrast ratios (≥4.5:1) | High |
| 8 | SEO | Add meta description + canonical | High |
| 9 | Best Practices | HTTPS everywhere | High |
| 10 | Best Practices | Avoid `document.write()` | Medium |
| 11 | PWA | Register service worker + icons | High |

---

## Performance Opportunities

| Opportunity | Savings | How |
|-------------|---------|-----|
| Eliminate render-blocking resources | 200ms | Defer non-critical CSS/JS |
| Properly size images | 150KB | Resize |
| Serve next-gen formats | 100KB | WebP/AVIF |
| Reduce unused JS | 80KB | Tree shaking |
| Text compression | 50KB | Brotli/gzip |

---

## Accessibility Quick Reference

| Category | Checks |
|----------|--------|
| **Names & Labels** | Form labels, alt text, button text |
| **Navigation** | Headings order, skip links |
| **Contrast** | Ratio ≥ 4.5:1 |
| **ARIA** | Proper ARIA attributes |
| **Tables** | Proper table markup |

---

## Lighthouse CI

```yaml
- name: Lighthouse CI
  uses: treosh/lighthouse-ci-action@v11
  with:
    urls: |
      https://example.com
      https://example.com/about
    budgetPath: ./lighthouse-budget.json
```

```json
[{
  "path": "/*",
  "timings": [
    { "metric": "first-contentful-paint", "budget": 2000 },
    { "metric": "largest-contentful-paint", "budget": 3000 },
    { "metric": "cumulative-layout-shift", "budget": 0.1 },
    { "metric": "total-blocking-time", "budget": 300 }
  ],
  "resourceSizes": [
    { "resourceType": "total", "budget": 500 },
    { "resourceType": "script", "budget": 200 }
  ]
}]
```

---

## Tips

| Tip | Mô tả |
|-----|--------|
| Test on mobile | Mobile score thường thấp hơn |
| Throttle CPU | Simulate slow device |
| Disable cache | See real loading time |
| Run multiple times | Scores vary |
| Use production build | Dev score thấp hơn |

---

Xem thêm: [Chrome DevTools Tổng Quan](19-chrome-devtools.md) | [Performance Panel](23-devtools-performance.md) | [Performance Optimization](33-performance-optimization.md)