# Fincount API Documentation

## Overview

**Fincount API** is a FastAPI-based backend service for the Fincount Flutter application, designed for fish counting and batch management in aquaculture operations.

- **Version**: 1.0.0
- **Base URL**: `https://your-domain.com` (or `http://localhost:8000` for local development)
- **Technology Stack**: FastAPI, SQLAlchemy, SQLite, JWT Authentication
- **Interactive Documentation**: Available at `/docs` (Swagger UI) and `/redoc` (ReDoc)

---

## Table of Contents

1. [Authentication](#authentication)
2. [Authentication Endpoints](#authentication-endpoints)
3. [Batches Endpoints](#batches-endpoints)
4. [Sessions Endpoints](#sessions-endpoints)
5. [Data Models](#data-models)
6. [Error Handling](#error-handling)
7. [Development Setup](#development-setup)

---

## Authentication

The API uses **JWT (JSON Web Token)** based authentication for protected endpoints.

### Getting a Token

1. Register a new user or login with existing credentials
2. Receive a JWT token in the response
3. Include the token in subsequent requests using the `Authorization` header:
   ```
   Authorization: Bearer <your_token_here>
   ```

### Token Details

- **Expiration**: 30 days (43200 minutes)
- **Token Type**: Bearer
- **Encoding**: HS256

---

## Authentication Endpoints

### 1. Register User

Create a new user account and receive an authentication token.

**Endpoint**: `POST /api/auth/register`

**Authentication**: Not required

**Request Body**:
```json
{
  "full_name": "John Doe",
  "username": "johndoe",
  "user_type": "Admin",
  "password": "securePassword123",
  "confirm_password": "securePassword123"
}
```

**Field Validations**:
- `full_name`: Required, string
- `username`: Required, unique, string
- `user_type`: Required, must be "Admin" or "Staff"
- `password`: Required, string
- `confirm_password`: Required, must match password

**Success Response** (201 Created):
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "fa1c3896-50a9-41b8-a573-a4c9dc1266bf",
    "full_name": "John Doe",
    "username": "johndoe",
    "user_type": "Admin",
    "createdAt": "2025-11-21T02:05:30.123456",
    "updatedAt": "2025-11-21T02:05:30.123456"
  }
}
```

**Error Responses**:
- `400 Bad Request`: Passwords don't match or invalid user type
- `400 Bad Request`: Username already registered

---

### 2. Login

Authenticate an existing user and receive a token.

**Endpoint**: `POST /api/auth/login`

**Authentication**: Not required

**Request Body**:
```json
{
  "username": "johndoe",
  "password": "securePassword123"
}
```

**Success Response** (200 OK):
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "fa1c3896-50a9-41b8-a573-a4c9dc1266bf",
    "full_name": "John Doe",
    "username": "johndoe",
    "user_type": "Admin",
    "createdAt": "2025-11-21T02:05:30.123456",
    "updatedAt": "2025-11-21T02:05:30.123456"
  }
}
```

**Error Responses**:
- `401 Unauthorized`: Incorrect username or password

---

### 3. Logout

Logout the current user (client-side token removal).

**Endpoint**: `POST /api/auth/logout`

**Authentication**: Required

**Headers**:
```
Authorization: Bearer <token>
```

**Success Response** (200 OK):
```json
{
  "message": "Logged out successfully"
}
```

---

## Batches Endpoints

### 1. Get All Batches

Retrieve a list of all batches.

**Endpoint**: `GET /api/batches`

**Authentication**: Not required

**Success Response** (200 OK):
```json
{
  "success": true,
  "data": {
    "batches": [
      {
        "id": "batch-uuid-1",
        "name": "Summer Batch 2025",
        "description": "Main pond batch for summer season",
        "userId": "fa1c3896-50a9-41b8-a573-a4c9dc1266bf",
        "totalCount": 5000,
        "createdAt": "2025-11-21T02:05:30.123456",
        "updatedAt": "2025-11-21T02:05:30.123456",
        "isActive": true
      }
    ]
  }
}
```

---

### 2. Create Batch

Create a new batch.

**Endpoint**: `POST /api/batches`

**Authentication**: Not required (uses default admin user)

**Request Body**:
```json
{
  "name": "Winter Batch 2025",
  "description": "New batch for winter season",
  "isActive": true
}
```

**Success Response** (201 Created):
```json
{
  "id": "new-batch-uuid",
  "name": "Winter Batch 2025",
  "description": "New batch for winter season",
  "userId": "fa1c3896-50a9-41b8-a573-a4c9dc1266bf",
  "totalCount": 0,
  "createdAt": "2025-11-21T02:10:30.123456",
  "updatedAt": "2025-11-21T02:10:30.123456",
  "isActive": true
}
```

---

### 3. Get Batch by ID

Retrieve a specific batch by its ID.

**Endpoint**: `GET /api/batches/{batch_id}`

**Authentication**: Required

**Headers**:
```
Authorization: Bearer <token>
```

**Success Response** (200 OK):
```json
{
  "id": "batch-uuid-1",
  "name": "Summer Batch 2025",
  "description": "Main pond batch for summer season",
  "userId": "fa1c3896-50a9-41b8-a573-a4c9dc1266bf",
  "totalCount": 5000,
  "createdAt": "2025-11-21T02:05:30.123456",
  "updatedAt": "2025-11-21T02:05:30.123456",
  "isActive": true
}
```

**Error Responses**:
- `404 Not Found`: Batch not found

---

### 4. Update Batch

Update an existing batch.

**Endpoint**: `PUT /api/batches/{batch_id}`

**Authentication**: Required

**Headers**:
```
Authorization: Bearer <token>
```

**Request Body** (all fields optional):
```json
{
  "name": "Updated Batch Name",
  "description": "Updated description",
  "isActive": false
}
```

**Success Response** (200 OK):
```json
{
  "id": "batch-uuid-1",
  "name": "Updated Batch Name",
  "description": "Updated description",
  "userId": "fa1c3896-50a9-41b8-a573-a4c9dc1266bf",
  "totalCount": 5000,
  "createdAt": "2025-11-21T02:05:30.123456",
  "updatedAt": "2025-11-21T02:15:30.123456",
  "isActive": false
}
```

**Error Responses**:
- `404 Not Found`: Batch not found

---

### 5. Delete Batch

Delete a batch permanently.

**Endpoint**: `DELETE /api/batches/{batch_id}`

**Authentication**: Required

**Headers**:
```
Authorization: Bearer <token>
```

**Success Response** (200 OK):
```json
{
  "message": "Batch deleted successfully"
}
```

**Error Responses**:
- `404 Not Found`: Batch not found

---

## Sessions Endpoints

### 1. Get All Sessions

Retrieve a list of all counting sessions.

**Endpoint**: `GET /api/sessions`

**Authentication**: Not required

**Success Response** (200 OK):
```json
{
  "success": true,
  "data": {
    "sessions": [
      {
        "id": "session-uuid-1",
        "batchId": "batch-uuid-1",
        "species": "Tilapia",
        "location": "Cagangohan",
        "notes": "First count of the day",
        "counts": {
          "Fish": 1500
        },
        "timestamp": "2025-11-21T08:30:00",
        "imageUrl": "https://example.com/image.jpg"
      }
    ],
    "pagination": {
      "total": 1,
      "page": 1,
      "limit": 100
    }
  }
}
```

---

### 2. Create Session

Create a new counting session. Auto-creates batch if it doesn't exist.

**Endpoint**: `POST /api/sessions`

**Authentication**: Not required (uses default admin user if userId not provided)

**Request Body**:
```json
{
  "batchId": "batch-uuid-1",
  "species": "Tilapia",
  "location": "Cagangohan",
  "notes": "Morning count session",
  "counts": {
    "Fish": 1250
  },
  "timestamp": "2025-11-21T08:30:00",
  "imageUrl": "https://example.com/image.jpg",
  "userId": "optional-user-uuid"
}
```

**Field Validations**:
- `batchId`: Required, string (batch will be auto-created if doesn't exist)
- `species`: Required, must be one of: "Tilapia", "Bangus (Milkfish)"
- `location`: Required, must be one of: "Cagangohan", "Southern"
- `notes`: Required, string
- `counts`: Required, object with string keys and integer values
- `timestamp`: Required, ISO 8601 datetime string
- `imageUrl`: Optional, string
- `userId`: Optional, string (defaults to first admin user)

**Success Response** (201 Created):
```json
{
  "success": true,
  "data": {
    "id": "new-session-uuid",
    "batchId": "batch-uuid-1",
    "species": "Tilapia",
    "location": "Cagangohan",
    "notes": "Morning count session",
    "counts": {
      "Fish": 1250
    },
    "timestamp": "2025-11-21T08:30:00",
    "imageUrl": "https://example.com/image.jpg"
  },
  "message": "Session created successfully"
}
```

**Error Responses**:
- `404 Not Found`: User not found (if userId provided doesn't exist)
- `422 Unprocessable Entity`: Invalid species or location value
- `500 Internal Server Error`: No users found in database

---

### 3. Get Sessions by Batch

Retrieve all sessions for a specific batch.

**Endpoint**: `GET /api/sessions/batch/{batch_id}`

**Authentication**: Required

**Headers**:
```
Authorization: Bearer <token>
```

**Success Response** (200 OK):
```json
[
  {
    "id": "session-uuid-1",
    "batchId": "batch-uuid-1",
    "species": "Tilapia",
    "location": "Cagangohan",
    "notes": "First count",
    "counts": {
      "Fish": 1500
    },
    "timestamp": "2025-11-21T08:30:00",
    "imageUrl": ""
  }
]
```

---

### 4. Update Session

Update an existing counting session.

**Endpoint**: `PUT /api/sessions/{session_id}`

**Authentication**: Required

**Headers**:
```
Authorization: Bearer <token>
```

**Request Body** (all fields optional):
```json
{
  "species": "Bangus (Milkfish)",
  "location": "Southern",
  "notes": "Updated notes",
  "counts": {
    "Fish": 1600
  }
}
```

**Success Response** (200 OK):
```json
{
  "id": "session-uuid-1",
  "batchId": "batch-uuid-1",
  "species": "Bangus (Milkfish)",
  "location": "Southern",
  "notes": "Updated notes",
  "counts": {
    "Fish": 1600
  },
  "timestamp": "2025-11-21T08:30:00",
  "imageUrl": ""
}
```

**Error Responses**:
- `404 Not Found`: Session not found

---

### 5. Delete Session

Delete a counting session permanently.

**Endpoint**: `DELETE /api/sessions/{session_id}`

**Authentication**: Required

**Headers**:
```
Authorization: Bearer <token>
```

**Success Response** (200 OK):
```json
{
  "message": "Session deleted successfully"
}
```

**Error Responses**:
- `404 Not Found`: Session not found

---

## Data Models

### User Model

```json
{
  "id": "uuid-string",
  "full_name": "string",
  "username": "string (unique)",
  "user_type": "Admin | Staff",
  "createdAt": "ISO 8601 datetime",
  "updatedAt": "ISO 8601 datetime"
}
```

---

### Batch Model

```json
{
  "id": "uuid-string",
  "name": "string",
  "description": "string (optional)",
  "userId": "uuid-string",
  "totalCount": "integer",
  "createdAt": "ISO 8601 datetime",
  "updatedAt": "ISO 8601 datetime",
  "isActive": "boolean"
}
```

---

### Session Model

```json
{
  "id": "uuid-string",
  "batchId": "uuid-string",
  "species": "Tilapia | Bangus (Milkfish)",
  "location": "Cagangohan | Southern",
  "notes": "string",
  "counts": {
    "Fish": "integer"
  },
  "timestamp": "ISO 8601 datetime string",
  "imageUrl": "string (optional)"
}
```

---

### Valid Enum Values

**Species**:
- `Tilapia`
- `Bangus (Milkfish)`

**Location**:
- `Cagangohan`
- `Southern`

---

## Error Handling

### HTTP Status Codes

- `200 OK`: Successful GET, PUT, DELETE requests
- `201 Created`: Successful POST requests
- `400 Bad Request`: Invalid request data or validation errors
- `401 Unauthorized`: Authentication required or invalid credentials
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation error (invalid enum values)
- `500 Internal Server Error`: Server-side errors

### Error Response Format

```json
{
  "detail": "Error message describing what went wrong"
}
```

### Common Errors

**Authentication Errors**:
```json
{
  "detail": "Incorrect username or password"
}
```

**Validation Errors**:
```json
{
  "detail": "Passwords do not match"
}
```

**Not Found Errors**:
```json
{
  "detail": "Batch not found"
}
```

**Enum Validation Errors**:
```json
{
  "detail": "Invalid species 'InvalidSpecies'. Must be one of: Tilapia, Bangus (Milkfish)"
}
```

---

## Development Setup

### Local Development

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Environment Variables**:
   Create a `.env` file based on `.env.example`:
   ```bash
   cp .env.example .env
   ```

3. **Run the Server**:
   ```bash
   python main.py
   ```
   Server will start at `http://localhost:8000`

4. **Access Interactive Documentation**:
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

### Database

- **Type**: SQLite
- **File**: `fincount.db`
- **Migrations**: Managed with Alembic

### Health Check

**Endpoint**: `GET /api/health`

**Response**:
```json
{
  "status": "healthy",
  "timestamp": "2025-11-21T02:05:30.123456",
  "version": "1.0.0"
}
```

---

## CORS Configuration

The API is configured to accept requests from all origins (`*`). In production, configure specific domains:

```python
allow_origins=["https://your-flutter-app.com"]
```

---

## Additional Resources

- **GitHub Repository**: https://github.com/Nevram30/fincount-api
- **Railway Deployment**: See `DEPLOYMENT.md` for deployment instructions
- **Database Setup**: See `DATABASE_SETUP.md` for database configuration

---

## Support

For issues or questions, please open an issue on the GitHub repository.

**Last Updated**: November 21, 2025
