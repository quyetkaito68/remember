# Templates tham khảo cho Markdown Doc Generator

Mỗi template là một cấu trúc markdown có sẵn các section chuẩn. Skill sẽ điền dữ liệu vào các placeholder.

---

## 1. README Template (`readme`)

```markdown
# {project_name}

> {one_line_description}

[![License]({license_badge})]({license_url})
[![Build Status]({ci_badge})]({ci_url})
[![Version]({version_badge})]({release_url})

---

## Mục lục
- [Tổng quan](#tổng-quan)
- [Tính năng](#tính-năng)
- [Kiến trúc](#kiến-trúc)
- [Cài đặt](#cài-đặt)
- [Cấu hình](#cấu-hình)
- [Sử dụng](#sử-dụng)
- [API Reference](#api-reference)
- [Testing](#testing)
- [Đóng góp](#đóng-góp)
- [License](#license)

---

## Tổng quan

{mô_tả_chi_tiết_2_3_câu}

### Tech Stack

| Thành phần | Công nghệ | Phiên bản |
|------------|-----------|-----------|
| Language   | {language} | {version} |
| Framework  | {framework} | {version} |
| Database   | {database} | {version} |
| Build Tool | {build_tool} | {version} |

---

## Tính năng

- ✅ {feature_1}
- ✅ {feature_2}
- ✅ {feature_3}
- 🚧 {planned_feature} (đang phát triển)

---

## Kiến trúc

```text
{architecture_diagram}
```

### Cấu trúc thư mục

```text
{folder_tree}
```

---

## Cài đặt

### Yêu cầu trước
- {requirement_1} (>= {version})
- {requirement_2} (>= {version})

### Các bước cài đặt

```bash
# Clone repository
git clone {repo_url}
cd {project_name}

# Cài dependencies
{install_command}

# Build (nếu cần)
{build_command}
```

---

## Cấu hình

Tạo file `.env` từ mẫu:

```bash
cp .env.example .env
```

Các biến môi trường quan trọng:

| Biến | Mô tả | Mặc định | Bắt buộc |
|------|-------|----------|----------|
| `{VAR_NAME}` | {description} | `{default}` | Yes/No |

---

## Sử dụng

### Chạy development

```bash
{dev_command}
```

### Chạy production

```bash
{prod_command}
```

### Ví dụ cơ bản

```{language}
// Example code
{code_snippet}
```

---

## API Reference

Xem chi tiết tại [API Documentation](API_DOCS.md) hoặc chạy:

```bash
{doc_command}
```

### Endpoints chính

| Method | Endpoint | Mô tả | Auth |
|--------|----------|-------|------|
| GET    | `/api/health` | Health check | No |
| POST   | `/api/auth/login` | Đăng nhập | No |
| GET    | `/api/users/me` | Thông tin user | Yes |

---

## Testing

```bash
# Chạy tất cả test
{test_command}

# Chạy test với coverage
{coverage_command}

# Chạy test watch mode
{watch_command}
```

### Coverage hiện tại
- Statements: {coverage_stmt}%
- Branches: {coverage_branch}%
- Functions: {coverage_func}%
- Lines: {coverage_line}%

---

## Đóng góp

Xem [CONTRIBUTING.md](CONTRIBUTING.md) để biết quy trình đóng góp.

### Quy trình nhanh
1. Fork repository
2. Tạo branch: `git checkout -b feature/tên-tính-năng`
3. Commit: `git commit -m "feat: mô tả thay đổi"`
4. Push: `git push origin feature/tên-tính-năng`
5. Tạo Pull Request

---

## License

Distributed under the {license_name} License. See `LICENSE` for more information.

---

## Liên hệ

- **Tác giả**: {author_name} - {author_email}
- **Project Link**: {repo_url}
- **Issues**: {issues_url}

---

*Tài liệu được tạo tự động bởi Markdown Doc Generator - {date} *
```

---

## 2. API Documentation Template (`api-docs`)

```markdown
# {project_name} - API Documentation

> Base URL: `{base_url}` | Version: `{version}`

---

## Xác thực (Authentication)

{auth_description}

### Header bắt buộc
```
Authorization: Bearer {token}
Content-Type: application/json
```

### Lấy Access Token
```bash
curl -X POST {base_url}/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "secret"}'
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "Bearer",
  "expires_in": 3600
}
```

---

## Error Handling

Tất cả error response tuân theo format:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Mô tả lỗi tiếng Việt",
    "details": {}
  }
}
```

### Mã lỗi phổ biến

| Code | HTTP Status | Mô tả |
|------|-------------|-------|
| `VALIDATION_ERROR` | 400 | Dữ liệu đầu vào không hợp lệ |
| `UNAUTHORIZED` | 401 | Chưa đăng nhập hoặc token hết hạn |
| `FORBIDDEN` | 403 | Không có quyền truy cập |
| `NOT_FOUND` | 404 | Tài nguyên không tồn tại |
| `INTERNAL_ERROR` | 500 | Lỗi server nội bộ |

---

## Endpoints

### {Module Name} - {module_description}

#### {Operation Name}
`{METHOD} {endpoint_path}`

**Mô tả**: {description}

**Headers**:
```
Authorization: Bearer <token>
```

**Path Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `{param}` | string | Yes | {description} |

**Query Parameters**:
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `{param}` | string | No | `{default}` | {description} |

**Request Body** (application/json):
```json
{
  "field1": "type",
  "field2": "type"
}
```

**Response** (200 OK):
```json
{
  "field1": "value",
  "field2": "value"
}
```

**Response** (400 Bad Request):
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Dữ liệu không hợp lệ",
    "details": {
      "field1": "Trường này là bắt buộc"
    }
  }
}
```

---

## Schemas (Data Models)

### {ModelName}

```json
{
  "id": "uuid",
  "name": "string",
  "email": "string",
  "created_at": "ISO8601 datetime",
  "updated_at": "ISO8601 datetime"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | uuid | Yes | Định danh duy nhất |
| `name` | string | Yes | Tên hiển thị |
| `email` | string | Yes | Email liên hệ |
| `created_at` | datetime | Yes | Thời gian tạo |
| `updated_at` | datetime | Yes | Thời gian cập nhật |

---

## Rate Limiting

- **Default**: {rate_limit} requests/{window}
- **Headers**:
  - `X-RateLimit-Limit`: Giới hạn
  - `X-RateLimit-Remaining`: Còn lại
  - `X-RateLimit-Reset`: Thời gian reset (Unix timestamp)

---

## Webhooks (nếu có)

### Cấu hình
URL: `{webhook_url}`
Events: `{event_list}`

### Payload mẫu
```json
{
  "event": "user.created",
  "timestamp": "2026-01-15T10:30:00Z",
  "data": { ... }
}
```

---

*Tài liệu được tạo tự động bởi Markdown Doc Generator - {date}*
```

---

## 3. Architecture Decision Record Template (`architecture` / `adr`)

```markdown
# ADR-{number}: {title}

> **Status**: {Proposed | Accepted | Rejected | Deprecated | Superseded}
> **Date**: {YYYY-MM-DD}
> **Deciders**: {names}
> **Technical Story**: {link_to_ticket}

---

## Context (Bối cảnh)

{Mô tả vấn đề, bối cảnh kỹ thuật, constraints buộc phải giải quyết}

### Yêu cầu
- {requirement_1}
- {requirement_2}

### Ràng buộc
- {constraint_1}
- {constraint_2}

---

## Decision (Quyết định)

**Chúng ta quyết định**: {mô tả quyết định ngắn gọn}

### Giải pháp được chọn

```text
{architecture_diagram}
```

### Giải pháp thay thế đã xem xét

| Giải pháp | Ưu điểm | Nhược điểm | Lý do không chọn |
|-----------|---------|------------|------------------|
| {alt_1} | {pros} | {cons} | {reason} |
| {alt_2} | {pros} | {cons} | {reason} |

---

## Consequences (Hệ quả)

### Tích cực
- {positive_1}
- {positive_2}

### Tiêu cực / Rủi ro
- {negative_1} - *Mitigation: {mitigation}*
- {negative_2} - *Mitigation: {mitigation}*

### Phụ thuộc mới
- {dependency_1}
- {dependency_2}

---

## Implementation Plan (Kế hoạch triển khai)

- [ ] Task 1: {description}
- [ ] Task 2: {description}
- [ ] Task 3: {description}

---

## References

- [Link 1]({url}) - {description}
- [Link 2]({url}) - {description}

---

*Tài liệu được tạo tự động bởi Markdown Doc Generator - {date}*
```

---

## 4. Changelog Template (`changelog`)

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added
- {feature_description}

### Changed
- {change_description}

### Deprecated
- {deprecated_feature}

### Removed
- {removed_feature}

### Fixed
- {bug_fix_description}

### Security
- {security_fix_description}

---

## [{version}] - {YYYY-MM-DD}

### Added
- {feature_description}

### Changed
- {change_description}

### Fixed
- {bug_fix_description}

---

## [{previous_version}] - {YYYY-MM-DD}
...

---

*Tài liệu được tạo tự động bởi Markdown Doc Generator - {date}*
```

---

## 5. Contributing Guide Template (`contributing`)

```markdown
# Contributing Guide

Cảm ơn bạn quan tâm đóng góp cho {project_name}! 🎉

---

## Code of Conduct

Dự án này tuân thủ [Contributor Covenant](CODE_OF_CONDUCT.md). Bằng cách tham gia, bạn đồng ý tuân thủ quy tắc ứng xử này.

---

## Cách đóng góp

### Báo lỗi (Bug Report)

Trước khi tạo issue, hãy kiểm tra:
- [ ] Issue chưa được báo cáo
- [ ] Đã thử reproduce trên phiên bản mới nhất
- [ ] Cung cấp thông tin đủ: OS, version, steps to reproduce, expected vs actual

Sử dụng template: `.github/ISSUE_TEMPLATE/bug_report.md`

### Đề xuất tính năng (Feature Request)

Sử dụng template: `.github/ISSUE_TEMPLATE/feature_request.md`

### Pull Request

1. Fork & clone
2. Tạo branch: `git checkout -b feature/tên-tính-năng`
3. Code + test
4. Commit theo convention (xem dưới)
5. Push & tạo PR

---

## Development Setup

```bash
# Clone fork của bạn
git clone https://github.com/{your-username}/{repo}.git
cd {repo}

# Add upstream
git remote add upstream https://github.com/{owner}/{repo}.git

# Cài đặt
{install_command}

# Chạy test
{test_command}

# Chạy linter
{lint_command}
```

---

## Commit Convention

Tuân thủ [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Types
| Type | Mô tả | Ví dụ |
|------|-------|-------|
| `feat` | Tính năng mới | `feat(auth): thêm OAuth2 login` |
| `fix` | Sửa lỗi | `fix(api): handle null pointer` |
| `docs` | Thay đổi docs | `docs(readme): cập nhật cài đặt` |
| `style` | Format code | `style: format theo prettier` |
| `refactor` | Refactor không thay đổi behavior | `refactor(utils): tách helper functions` |
| `test` | Thêm/sửa test | `test(auth): thêm unit test login` |
| `chore` | Build, deps, config | `chore(deps): update lodash` |

### Scope (phạm vi)
- `auth`, `api`, `ui`, `db`, `config`, `ci`, `docs`, `test`, `deps`...

---

## Coding Standards

### Language-specific
- **TypeScript**: Strict mode, ESLint + Prettier
- **Python**: Black, Ruff, type hints
- **Go**: gofmt, golangci-lint
- **Rust**: rustfmt, clippy

### General
- [ ] Code có comment cho logic phức tạp
- [ ] Không hardcode secrets/config
- [ ] Xử lý error đúng cách
- [ ] Test coverage ≥ 80% cho code mới

---

## Review Process

1. **Automated checks**: CI phải pass (test, lint, type-check)
2. **Code review**: Ít nhất 1 reviewer approve
3. **Merge**: Squash & merge vào `main`

### Review checklist
- [ ] Code giải quyết đúng vấn đề
- [ ] Không breaking change (hoặc đã document)
- [ ] Test đủ (unit + integration nếu cần)
- [ ] Docs đã cập nhật
- [ ] Performance OK

---

## Release Process

1. Maintainer tạo release branch: `release/v{x.y.z}`
2. Update version, changelog
3. Tạo tag: `git tag v{x.y.z}`
4. CI/CD tự động publish

---

## Liên hệ

- **Maintainers**: @{maintainer1}, @{maintainer2}
- **Discord/Slack**: {link}
- **Email**: {email}

---

*Tài liệu được tạo tự động bởi Markdown Doc Generator - {date}*
```

---

## 6. Technical Specification Template (`tech-spec`)

```markdown
# Technical Specification: {title}

> **Author**: {author}
> **Status**: {Draft | Review | Approved | Implemented | Deprecated}
> **Created**: {YYYY-MM-DD}
> **Updated**: {YYYY-MM-DD}
> **Reviewers**: {names}

---

## 1. Overview (Tổng quan)

### 1.1 Purpose (Mục đích)
{Mô tả 1-2 câu về vấn đề cần giải quyết}

### 1.2 Scope (Phạm vi)
- In scope: {items}
- Out of scope: {items}

### 1.3 Definitions (Định nghĩa)
| Thuật ngữ | Định nghĩa |
|-----------|------------|
| {term} | {definition} |

---

## 2. Requirements (Yêu cầu)

### 2.1 Functional Requirements (Yêu cầu chức năng)
| ID | Requirement | Priority |
|----|-------------|----------|
| FR-01 | {description} | High/Medium/Low |
| FR-02 | {description} | High/Medium/Low |

### 2.2 Non-Functional Requirements (Yêu cầu phi chức năng)
| ID | Requirement | Target |
|----|-------------|--------|
| NFR-01 | Latency < {ms}ms | P99 |
| NFR-02 | Availability {99.9}% | Monthly |
| NFR-03 | Throughput {req/s} | Peak |

---

## 3. Architecture (Kiến trúc)

### 3.1 High-Level Design
```text
{architecture_diagram}
```

### 3.2 Components
| Component | Responsibility | Technology |
|-----------|----------------|------------|
| {name} | {responsibility} | {tech} |

### 3.3 Data Flow
```text
{sequence_or_flow_diagram}
```

### 3.4 Data Models
```text
{er_diagram_or_schema}
```

---

## 4. API Design (nếu áp dụng)

### 4.1 Endpoints
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/resource` | List resources |

### 4.2 Request/Response
```json
// Request
{ "field": "value" }

// Response
{ "data": {...} }
```

---

## 5. Implementation Details (Chi tiết triển khai)

### 5.1 Key Algorithms / Logic
{Mô tả thuật toán/core logic quan trọng}

### 5.2 Error Handling
| Scenario | Handling Strategy |
|----------|-------------------|
| {scenario} | {strategy} |

### 5.3 Security Considerations
- {security_point_1}
- {security_point_2}

### 5.4 Performance Optimizations
- {optimization_1}
- {optimization_2}

---

## 6. Testing Strategy

### 6.1 Unit Tests
- Coverage target: ≥ {80}%
- Key areas: {modules}

### 6.2 Integration Tests
- Scenarios: {list}

### 6.3 E2E Tests
- Critical paths: {list}

### 6.4 Load/Stress Tests
- Tools: {tools}
- Targets: {targets}

---

## 7. Deployment & Operations

### 7.1 Deployment Architecture
```text
{deployment_diagram}
```

### 7.2 Configuration
| Config | Environment | Default |
|--------|-------------|---------|
| {key} | {env} | {value} |

### 7.3 Monitoring & Alerting
- Metrics: {metrics}
- Alerts: {alerts}
- Dashboards: {links}

### 7.4 Rollback Plan
{rollback_steps}

---

## 8. Migration Plan (nếu có)

### 8.1 Data Migration
{steps}

### 8.2 Backward Compatibility
{strategy}

### 8.3 Rollback Migration
{steps}

---

## 9. Open Questions / Risks

| Question/Risk | Impact | Mitigation | Owner |
|---------------|--------|------------|-------|
| {item} | High/Med/Low | {plan} | {name} |

---

## 10. References

- [Ref 1]({url}) - {description}
- [Ref 2]({url}) - {description}

---

*Tài liệu được tạo tự động bởi Markdown Doc Generator - {date}*
```

---

## 7. Meeting Notes / RFC Template (`meeting-notes`)

```markdown
# {Meeting Title / RFC Title}

> **Date**: {YYYY-MM-DD}
> **Time**: {HH:MM} - {HH:MM} (Timezone)
> **Attendees**: {names}
> **Facilitator**: {name}
> **Note Taker**: {name}

---

## Objective (Mục tiêu)
{Mô tả mục đích cuộc họp/RFC}

---

## Agenda (Chương trình)
1. {Topic 1} - {time} - {owner}
2. {Topic 2} - {time} - {owner}
3. {Topic 3} - {time} - {owner}

---

## Discussion Notes (Ghi chú thảo luận)

### {Topic 1}
**Key points**:
- {point_1}
- {point_2}

**Decisions**:
- {decision_1}

**Action Items**:
- [ ] {action} - @{assignee} - Due: {date}

---

### {Topic 2}
...

---

## Decisions Summary (Tóm tắt quyết định)
| # | Decision | Rationale | Owner |
|---|----------|-----------|-------|
| 1 | {decision} | {reason} | {name} |

---

## Action Items (Hành động)
| # | Action | Owner | Due Date | Status |
|---|--------|-------|----------|--------|
| 1 | {action} | @{name} | {YYYY-MM-DD} | ☐ Todo |

---

## Follow-up (Theo dõi)
- Next meeting: {date/time}
- Related docs: {links}
- Parking lot: {items deferred}

---

*Tài liệu được tạo tự động bởi Markdown Doc Generator - {date}*
```

---

## Cách sử dụng template

Trong SKILL.md, mode `template` sẽ:
1. Nhận template name từ user (readme, api-docs, architecture, changelog, contributing, tech-spec, meeting-notes)
2. Đọc template tương ứng từ file này
3. Thu thập dữ liệu từ project/context
4. Fill placeholders → Sinh file .md hoàn chỉnh

Placeholders dùng format `{placeholder_name}` - skill sẽ replace bằng giá trị thực.