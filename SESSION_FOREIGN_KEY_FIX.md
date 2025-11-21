# Session Foreign Key Fix - Summary

## Problem Identified

**Error Message:**
```
Failed to create session: (psycopg2.errors.ForeignKeyViolation) 
insert or update on table "batches" violates foreign key constraint "batches_user_id_fkey"
DETAIL: Key (user_id)=(fa1c3896-50a9-41b8-a573-a4c9dc1266bf) is not present in table "users"
```

## Root Cause

The API was using a **hardcoded user_id** (`fa1c3896-50a9-41b8-a573-a4c9dc1266bf`) that **did not exist in the database**.

### Where It Was Hardcoded:
1. **Line 95** in `router_sessions.py` - Batch creation
2. **Line 106** in `router_sessions.py` - Session creation

### The Problem Chain:
```
Hardcoded user_id (doesn't exist)
    ↓
Batch auto-created with invalid user_id
    ↓
Session tries to reference invalid batch
    ↓
FOREIGN KEY VIOLATION!
```

## Solution Implemented

### 1. **Updated Schema** (`schemas.py`)
Added optional `userId` field to `SessionBase`:
```python
class SessionBase(BaseModel):
    batchId: str
    species: SpeciesEnum
    location: LocationEnum
    notes: str
    counts: Dict[str, int]
    timestamp: str
    imageUrl: str
    userId: Optional[str] = None  # ✅ NEW: Optional user ID
```

### 2. **Updated Session Creation Logic** (`router_sessions.py`)

**Before (❌):**
```python
batch = Batch(
    id=session_data.batchId,
    name=f"Auto-created batch {session_data.batchId[:8]}",
    description="Automatically created from session",
    user_id="fa1c3896-50a9-41b8-a573-a4c9dc1266bf",  # ❌ Hardcoded!
    is_active=True
)

new_session = SessionModel(
    batch_id=session_data.batchId,
    user_id="fa1c3896-50a9-41b8-a573-a4c9dc1266bf",  # ❌ Hardcoded!
    ...
)
```

**After (✅):**
```python
# Get user_id from request or use default admin user
user_id = session_data.userId
if not user_id:
    # Use the first admin user as default
    default_user = db.query(User).filter(User.role == "admin").first()
    if not default_user:
        default_user = db.query(User).first()
    if not default_user:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No users found in database. Please create a user first."
        )
    user_id = default_user.id

# Validate that user exists
user = db.query(User).filter(User.id == user_id).first()
if not user:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User with id '{user_id}' not found."
    )

batch = Batch(
    id=session_data.batchId,
    name=f"Auto-created batch {session_data.batchId[:8]}",
    description="Automatically created from session",
    user_id=user_id,  # ✅ Validated user_id
    is_active=True
)

new_session = SessionModel(
    batch_id=session_data.batchId,
    user_id=user_id,  # ✅ Validated user_id
    ...
)
```

## Key Improvements

### ✅ User Validation
- Validates that user exists before creating batch/session
- Provides clear error messages when user not found

### ✅ Flexible User Assignment
- Accepts `userId` from Flutter app (for future authentication)
- Falls back to default admin user if not provided
- Works with existing database users

### ✅ Better Error Handling
- Returns 404 if user doesn't exist
- Returns 500 if no users in database at all
- Provides clear error messages for debugging

### ✅ Proper Logging
```python
logger.info(f"✓ User validated: {user.email} ({user.role})")
logger.info(f"✓ Batch created successfully with user_id: {user_id}")
logger.info(f"✓ Session created successfully: {new_session.id}")
logger.info(f"  User ID: {new_session.user_id}")
```

## Database Users (Current State)

```
ID: 2923dc80-0751-401e-a4c4-039be45fc2fb
Email: admin@fincount.com
Name: Admin User
Role: admin

ID: 30b72ff1-8666-415a-ab2e-998cc8f3b569
Email: user@fincount.com
Name: Test User
Role: user
```

## Testing Recommendations

### Test Case 1: Session Creation (Without userId)
```bash
curl -X POST http://localhost:8000/sessions \
  -H "Content-Type: application/json" \
  -d '{
    "batchId": "test-batch-001",
    "species": "Tilapia",
    "location": "Cagangohan",
    "notes": "Test session",
    "counts": {"Fish": 100},
    "timestamp": "2025-11-21T02:00:00Z",
    "imageUrl": ""
  }'
```
**Expected:** Uses default admin user (2923dc80-0751-401e-a4c4-039be45fc2fb)

### Test Case 2: Session Creation (With userId)
```bash
curl -X POST http://localhost:8000/sessions \
  -H "Content-Type: application/json" \
  -d '{
    "batchId": "test-batch-002",
    "species": "Bangus (Milkfish)",
    "location": "Southern",
    "notes": "Test with user",
    "counts": {"Fish": 50},
    "timestamp": "2025-11-21T02:00:00Z",
    "imageUrl": "",
    "userId": "30b72ff1-8666-415a-ab2e-998cc8f3b569"
  }'
```
**Expected:** Uses specified user

### Test Case 3: Invalid User ID
```bash
curl -X POST http://localhost:8000/sessions \
  -H "Content-Type: application/json" \
  -d '{
    "batchId": "test-batch-003",
    "species": "Tilapia",
    "location": "Cagangohan",
    "notes": "Invalid user test",
    "counts": {"Fish": 75},
    "timestamp": "2025-11-21T02:00:00Z",
    "imageUrl": "",
    "userId": "invalid-user-id"
  }'
```
**Expected:** Returns 404 error with message "User with id 'invalid-user-id' not found."

## Flutter App Changes (Optional)

To send userId from the app, update the session creation:

```dart
final session = Session(
  batchId: batchId,
  species: species,
  location: location,
  notes: notes,
  counts: counts,
  timestamp: timestamp,
  imageUrl: imageUrl,
  userId: currentUserId, // ✅ Add this
);
```

## Migration Notes

- **No database migration needed** - only code changes
- **Backward compatible** - works with or without userId in request
- **Uses existing database users** - no new users need to be created

## Files Modified

1. ✅ `schemas.py` - Added `userId: Optional[str]` to SessionBase
2. ✅ `router_sessions.py` - Added user validation and removed hardcoded user_id

## Status

✅ **FIX COMPLETE** - Ready for testing
