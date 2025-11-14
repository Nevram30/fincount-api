# Database Setup Guide

## Quick Start

### Local Development (SQLite)

```bash
# Run migrations
alembic upgrade head

# Seed initial users
python seed.py

# Start the server
uvicorn main:app --reload
```

### Railway Deployment (PostgreSQL)

The application is configured to automatically:
1. Detect the `DATABASE_URL` environment variable from Railway
2. Run migrations on startup
3. Seed initial users if database is empty

See [DEPLOYMENT.md](DEPLOYMENT.md) for complete Railway deployment instructions.

## Database Commands

### Migrations

```bash
# Create a new migration after modifying models.py
alembic revision --autogenerate -m "Description of changes"

# Apply all pending migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# View migration history
alembic history

# View current version
alembic current
```

### Seeding Data

```bash
# Seed initial users (safe to run multiple times)
python seed.py
```

The seed script will:
- Create database tables if they don't exist
- Add two default users (admin and regular user)
- Skip seeding if users already exist

### Default Users

After seeding, you can login with:

**Admin User:**
- Email: `admin@fincount.com`
- Password: `admin123`
- Role: `admin`

**Test User:**
- Email: `user@fincount.com`
- Password: `user123`
- Role: `user`

⚠️ **Change these passwords in production!**

## Database Schema

### Users Table
- `id` (String, Primary Key) - UUID
- `email` (String, Unique) - User email
- `name` (String) - User full name
- `hashed_password` (String) - Bcrypt hashed password
- `role` (String) - User role (admin/user)
- `created_at` (DateTime)
- `updated_at` (DateTime)

### Batches Table
- `id` (String, Primary Key) - UUID
- `name` (String) - Batch name
- `description` (String, Optional)
- `user_id` (String, Foreign Key) - Owner user ID
- `total_count` (Integer) - Total count
- `is_active` (Boolean) - Active status
- `created_at` (DateTime)
- `updated_at` (DateTime)

### Sessions Table
- `id` (String, Primary Key) - UUID
- `batch_id` (String, Foreign Key) - Associated batch
- `user_id` (String, Foreign Key) - Owner user ID
- `species` (String) - Species name
- `location` (String) - Location
- `notes` (String, Optional) - Additional notes
- `counts` (JSON) - Count data (e.g., {"alive": 100, "dead": 5})
- `timestamp` (String) - Session timestamp
- `image_url` (String, Optional) - Image URL
- `created_at` (DateTime)

## Environment Variables

### Required for Production (Railway)
- `DATABASE_URL` - PostgreSQL connection string (automatically provided by Railway)

### Optional
- `SECRET_KEY` - JWT secret key (defaults to development key)

## Switching Databases

### From SQLite to PostgreSQL

1. Set the `DATABASE_URL` environment variable:
```bash
export DATABASE_URL="postgresql://user:password@localhost/fincount"
```

2. Run migrations:
```bash
alembic upgrade head
```

3. Seed data:
```bash
python seed.py
```

### From PostgreSQL to SQLite

1. Remove or unset `DATABASE_URL`:
```bash
unset DATABASE_URL
```

2. The app will automatically use SQLite (`fincount.db`)

## Troubleshooting

### Issue: "No such table" error
**Solution:** Run migrations
```bash
alembic upgrade head
```

### Issue: "User already exists" when seeding
**Solution:** This is normal. The seed script skips if users exist.

### Issue: Migration conflicts
**Solution:** Check migration history and resolve conflicts
```bash
alembic history
alembic current
```

### Issue: Database connection refused
**Solution:** 
- Check `DATABASE_URL` is correct
- Verify database server is running
- Check network connectivity

## Database Backup (Railway)

Railway automatically backs up PostgreSQL databases. To manually backup:

```bash
# Connect to Railway database
railway connect postgres

# Export data
pg_dump > backup.sql
```

## Additional Resources

- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Railway PostgreSQL Guide](https://docs.railway.app/databases/postgresql)
