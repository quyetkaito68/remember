---
title: Chrome DevTools Protocol (CDP)
description: "Chrome DevTools Protocol — giao thức communication giữa browser và tools: Puppeteer, Playwright, debugger đều dùng CDP"
tags: [cdp, chrome-devtools-protocol, websocket-debugging, devtools-protocol, browser-automation]
category: developer
updated: 2026-07-26
order: 27
---

# Chrome DevTools Protocol (CDP)

JSON-RPC over WebSocket — Puppeteer, Playwright, VS Code debugger đều dùng CDP.

---

## Architecture

```text
┌──────────────────┐  WebSocket  ┌──────────────────┐
│  Client          │ ◄═════════▶│  Chrome          │
│  (Puppeteer)     │ JSON-RPC    │  (Browser)       │
│                  │             │                  │
│  → {"id":1,      │             │  Process command │
│    "method":     │             │  Return result   │
│    "Page.navigate│             │  → {"id":1,      │
│    "params":{    │             │    "result":{}}  │
│     "url":"..."}}│             │                  │
└──────────────────┘             └──────────────────┘
```

---

## CDP Domains

| Domain | Capability | Key Commands |
|--------|-----------|--------------|
| **Page** | Navigate, screenshot, PDF | `Page.navigate`, `Page.captureScreenshot`, `Page.printToPDF` |
| **Runtime** | Execute JS | `Runtime.evaluate`, `Runtime.callFunctionOn` |
| **DOM** | Inspect/modify DOM | `DOM.getDocument`, `DOM.querySelector` |
| **Network** | Monitor/control requests | `Network.enable`, `Network.getResponseBody`, `Network.emulateNetworkConditions` |
| **Emulation** | Device/viewport/location | `Emulation.setDeviceMetricsOverride`, `Emulation.setGeolocationOverride` |
| **Input** | Dispatch events | `Input.dispatchMouseEvent`, `Input.dispatchKeyEvent` |
| **Debugger** | Breakpoints | `Debugger.enable`, `Debugger.setBreakpoint` |
| **Performance** | Profiling | `Performance.enable`, `Performance.getMetrics` |
| **Target** | Tab management | `Target.getTargets`, `Target.attachToTarget` |
| **Browser** | Browser-level | `Browser.getVersion`, `Browser.close` |

---

## Command Format

```json
// Request: {id, method, params}
→ {"id":1, "method":"Page.navigate", "params":{"url":"https://example.com"}}

// Response: {id, result}
← {"id":1, "result":{"frameId":"ABC123","loaderId":"XYZ789"}}

// Evaluate JS
→ {"id":2, "method":"Runtime.evaluate", "params":{"expression":"1+1"}}
← {"id":2, "result":{"result":{"type":"number","value":2}}}

// Screenshot
→ {"id":3, "method":"Page.captureScreenshot", "params":{"format":"png"}}
← {"id":3, "result":{"data":"base64..."}}

// Set viewport
→ {"method":"Emulation.setDeviceMetricsOverride", "params":{"width":375,"height":812,"deviceScaleFactor":3,"mobile":true}}
```

---

## Events

Chrome gửi events khi có thay đổi:

```json
← {"method":"Page.loadEventFired","params":{}}
← {"method":"Network.requestWillBeSent","params":{"requestId":"1","request":{"url":"https://api.example.com/data","method":"GET"}}}
← {"method":"Runtime.consoleAPICalled","params":{"type":"log","args":[{"type":"string","value":"Hello"}]}}
```

---

## Kết nối với Chrome

```bash
chrome --remote-debugging-port=9222        # Launch with debugging
ws://localhost:9222/devtools/browser/ABC123 # Connect WebSocket
chrome://inspect/#devices                   # Inspect targets
```

---

## Puppeteer ↔ CDP Mapping

| Puppeteer | CDP Command |
|-----------|-------------|
| `page.goto(url)` | `Page.navigate` |
| `page.screenshot()` | `Page.captureScreenshot` |
| `page.evaluate(fn)` | `Runtime.evaluate` |
| `page.click(sel)` | `Input.dispatchMouseEvent` |
| `page.setViewport()` | `Emulation.setDeviceMetricsOverride` |

### Direct CDP trong Puppeteer

```javascript
const client = await page.createCDPSession();
await client.send('Page.captureScreenshot', { format: 'png' });
client.on('Network.requestWillBeSent', (e) => console.log(e.request.url));
```

### Direct CDP trong Playwright

```javascript
const cdp = await page.context().newCDPSession(page);
await cdp.send('Performance.enable');
const metrics = await cdp.send('Performance.getMetrics');
```

---

## Security

| Risk | Mitigation |
|------|-----------|
| Unauthorized access | Only bind to localhost |
| Exposed port | Firewall, don't expose to network |
| Remote code execution | Don't run untrusted code via CDP |

---

Xem thêm: [Puppeteer & Playwright](28-puppeteer-playwright.md) | [Chrome DevTools Tổng Quan](19-chrome-devtools.md) | [Browser Automation](29-browser-automation.md)