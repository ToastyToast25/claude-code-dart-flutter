---
description: "Documents API endpoints with OpenAPI/Swagger format"
globs: ["docs/api/**/*.md", "openapi.yaml", "swagger.json"]
alwaysApply: false
---

# API Documentation Skill

Document API endpoints for consistency and reference.

## Trigger Keywords
- document api
- api docs
- endpoint docs
- api reference

---

## API Documentation Template

### Endpoint Definition

```markdown
## [Endpoint Name]

**[METHOD]** `/api/v1/[resource]`

[Brief description of what this endpoint does]

### Authentication
- Required: Yes/No
- Type: Bearer Token / API Key / None

### Request

#### Headers
| Header | Type | Required | Description |
|--------|------|----------|-------------|
| Authorization | string | Yes | Bearer token |
| Content-Type | string | Yes | application/json |

#### Path Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| id | string | Yes | Resource ID |

#### Query Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| page | int | No | 1 | Page number |
| limit | int | No | 20 | Items per page |
| sort | string | No | created_at | Sort field |

#### Request Body
```json
{
  "field1": "string",
  "field2": 123,
  "nested": {
    "subfield": true
  }
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| field1 | string | Yes | Description |
| field2 | number | No | Description |
| nested.subfield | boolean | No | Description |

### Response

#### Success (200 OK)
```json
{
  "data": {
    "id": "abc-123",
    "field1": "value",
    "createdAt": "2024-01-15T10:30:00Z"
  },
  "meta": {
    "timestamp": "2024-01-15T10:30:00Z"
  }
}
```

#### Error Responses
| Status | Code | Description |
|--------|------|-------------|
| 400 | BAD_REQUEST | Invalid request body |
| 401 | UNAUTHORIZED | Missing or invalid token |
| 403 | FORBIDDEN | Insufficient permissions |
| 404 | NOT_FOUND | Resource not found |
| 500 | SERVER_ERROR | Internal server error |

#### Error Response Format
```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "User not found",
    "details": {}
  }
}
```

### Example

#### Request
```bash
curl -X POST https://api.example.com/api/v1/users \
  -H "Authorization: Bearer token123" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "name": "John Doe"
  }'
```

#### Response
```json
{
  "data": {
    "id": "user-123",
    "email": "user@example.com",
    "name": "John Doe",
    "createdAt": "2024-01-15T10:30:00Z"
  }
}
```
```

---

## Full API Reference Structure

```markdown
# API Reference

## Overview
- Base URL: `https://api.example.com`
- Version: v1
- Format: JSON

## Authentication
All endpoints require authentication unless marked as public.

### Bearer Token
```
Authorization: Bearer <token>
```

### Obtaining a Token
See [Authentication](#authentication-endpoints) section.

---

## Rate Limiting
- **Limit**: 100 requests per minute
- **Headers**:
  - `X-RateLimit-Limit`: Total allowed requests
  - `X-RateLimit-Remaining`: Remaining requests
  - `X-RateLimit-Reset`: Unix timestamp for reset

---

## Common Response Codes

| Code | Status | Description |
|------|--------|-------------|
| 200 | OK | Request succeeded |
| 201 | Created | Resource created |
| 204 | No Content | Success, no response body |
| 400 | Bad Request | Invalid request |
| 401 | Unauthorized | Authentication required |
| 403 | Forbidden | Permission denied |
| 404 | Not Found | Resource not found |
| 422 | Unprocessable Entity | Validation failed |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server error |

---

## Pagination

Paginated responses include:
```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100,
    "totalPages": 5,
    "hasNext": true,
    "hasPrev": false
  }
}
```

Query parameters:
- `page`: Page number (default: 1)
- `limit`: Items per page (default: 20, max: 100)

---

## Endpoints

### Authentication Endpoints

#### Login
**POST** `/api/v1/auth/login`
[Details...]

#### Register
**POST** `/api/v1/auth/register`
[Details...]

### User Endpoints

#### List Users
**GET** `/api/v1/users`
[Details...]

#### Get User
**GET** `/api/v1/users/:id`
[Details...]

#### Create User
**POST** `/api/v1/users`
[Details...]

#### Update User
**PUT** `/api/v1/users/:id`
[Details...]

#### Delete User
**DELETE** `/api/v1/users/:id`
[Details...]
```

---

## OpenAPI/Swagger Specification

```yaml
# openapi.yaml
openapi: 3.0.3
info:
  title: My API
  description: API documentation for My App
  version: 1.0.0
  contact:
    email: api@example.com

servers:
  - url: https://api.example.com
    description: Production
  - url: https://staging-api.example.com
    description: Staging
  - url: http://localhost:3000
    description: Development

security:
  - bearerAuth: []

paths:
  /api/v1/users:
    get:
      summary: List all users
      tags:
        - Users
      parameters:
        - name: page
          in: query
          schema:
            type: integer
            default: 1
        - name: limit
          in: query
          schema:
            type: integer
            default: 20
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserListResponse'
        '401':
          $ref: '#/components/responses/Unauthorized'

    post:
      summary: Create a new user
      tags:
        - Users
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateUserRequest'
      responses:
        '201':
          description: User created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserResponse'
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'

  /api/v1/users/{id}:
    get:
      summary: Get user by ID
      tags:
        - Users
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserResponse'
        '404':
          $ref: '#/components/responses/NotFound'

components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

  schemas:
    User:
      type: object
      properties:
        id:
          type: string
          example: "user-123"
        email:
          type: string
          format: email
        name:
          type: string
        createdAt:
          type: string
          format: date-time
        updatedAt:
          type: string
          format: date-time

    CreateUserRequest:
      type: object
      required:
        - email
        - name
      properties:
        email:
          type: string
          format: email
        name:
          type: string
          minLength: 1
          maxLength: 100
        password:
          type: string
          minLength: 8

    UserResponse:
      type: object
      properties:
        data:
          $ref: '#/components/schemas/User'

    UserListResponse:
      type: object
      properties:
        data:
          type: array
          items:
            $ref: '#/components/schemas/User'
        pagination:
          $ref: '#/components/schemas/Pagination'

    Pagination:
      type: object
      properties:
        page:
          type: integer
        limit:
          type: integer
        total:
          type: integer
        totalPages:
          type: integer

    Error:
      type: object
      properties:
        error:
          type: object
          properties:
            code:
              type: string
            message:
              type: string

  responses:
    BadRequest:
      description: Bad request
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
    Unauthorized:
      description: Unauthorized
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
    NotFound:
      description: Resource not found
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
```

---

## API Endpoint Registry

Maintain a central registry of all endpoints in the project:

```markdown
# API Endpoint Registry

## v1 Endpoints

| Method | Path | Handler | Auth | Description |
|--------|------|---------|------|-------------|
| POST | /api/v1/auth/login | AuthHandler.login | No | User login |
| POST | /api/v1/auth/register | AuthHandler.register | No | User registration |
| POST | /api/v1/auth/logout | AuthHandler.logout | Yes | User logout |
| POST | /api/v1/auth/refresh | AuthHandler.refresh | No | Refresh token |
| GET | /api/v1/users | UserHandler.list | Yes | List users |
| GET | /api/v1/users/:id | UserHandler.get | Yes | Get user |
| POST | /api/v1/users | UserHandler.create | Yes | Create user |
| PUT | /api/v1/users/:id | UserHandler.update | Yes | Update user |
| DELETE | /api/v1/users/:id | UserHandler.delete | Yes | Delete user |
| GET | /api/v1/products | ProductHandler.list | Yes | List products |
| GET | /api/v1/products/:id | ProductHandler.get | Yes | Get product |

## WebSocket Endpoints

| Path | Event | Description |
|------|-------|-------------|
| /ws | connect | Establish connection |
| /ws | message | Send/receive messages |
| /ws | notification | Real-time notifications |

## Webhook Endpoints

| Method | Path | Provider | Description |
|--------|------|----------|-------------|
| POST | /webhooks/stripe | Stripe | Payment events |
| POST | /webhooks/github | GitHub | Repository events |
```

---

## File Location

```
docs/
├── api/
│   ├── README.md           # API overview
│   ├── authentication.md   # Auth details
│   ├── endpoints/
│   │   ├── users.md
│   │   ├── products.md
│   │   └── orders.md
│   └── openapi.yaml        # OpenAPI spec
```

---

## Checklist

- [ ] All endpoints documented
- [ ] Request/response examples provided
- [ ] Error codes documented
- [ ] Authentication requirements clear
- [ ] Rate limits documented
- [ ] OpenAPI spec up to date
- [ ] Endpoint registry maintained
- [ ] Versioning strategy documented
