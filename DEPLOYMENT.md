# Railway Deployment Guide for Fincount API

This guide will help you deploy your FastAPI application to Railway with PostgreSQL database.

## Prerequisites

- Railway account (sign up at https://railway.app)
- Git repository with your code
- GitHub account (for connecting to Railway)

## Step 1: Prepare Your Application

✅ Your application is already configured with:
- Environment variable support for `DATABASE_URL`
- PostgreSQL driver (`psycopg2-binary`)
- Alembic migrations
- CORS middleware for Flutter app
- Seed script for initial users

## Step 2: Deploy to Railway

### Option A: Deploy via Railway Dashboard

1. **Go to Railway Dashboard**
   - Visit https://railway.app
   - Click "New Project"

2. **Add PostgreSQL Database**
   - Click "Add Service" → "Database" → "PostgreSQL"
   - Railway will automatically create a PostgreSQL database
   - The `DATABASE_URL` environment variable will be automatically set

3. **Deploy Your API**
   - Click "Add Service" → "GitHub Repo"
   - Select your `fincount-api` repository
   - Railway will automatically detect it's a Python app

4. **Configure Build Settings** (if needed)
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Option B: Deploy via Railway CLI

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Initialize project
railway init

# Add PostgreSQL
railway add --database postgresql

# Deploy
railway up
```

## Step 3: Run Database Migrations

After deployment, you need to run migrations and seed data:

### Using Railway CLI:

```bash
# Connect to your Railway project
railway link

# Run migrations
railway run alembic upgrade head

# Seed initial users
railway run python seed.py
```

### Using Railway Dashboard:

1. Go to your API service in Railway
2. Click on "Settings" → "Deploy"
3. Add a custom start command that runs migrations first:

```bash
alembic upgrade head && python seed.py && uvicorn main:app --host 0.0.0.0 --port $PORT
```

## Step 4: Environment Variables

Railway automatically provides:
- `DATABASE_URL` - PostgreSQL connection string
- `PORT` - Port number for your application

**IMPORTANT: Add SECRET_KEY for production:**

1. Generate a secure secret key:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

2. Add to Railway:
   - Go to your service in Railway Dashboard
   - Click "Variables" tab
   - Add variable:
     - Name: `SECRET_KEY`
     - Value: (paste your generated key)

Example:
```
SECRET_KEY=Kihqm8wAXCAZXMCba4T61IMpsqrVvjV0bbjTBQKqH3U
```

⚠️ **Never commit your SECRET_KEY to Git!**

## Step 5: Get Your API URL

1. In Railway Dashboard, go to your API service
2. Click "Settings" → "Networking"
3. Click "Generate Domain"
4. Your API will be available at: `https://your-app.railway.app`

## Step 6: Test Your Deployment

Test your API endpoints:

```bash
# Health check
curl https://your-app.railway.app/api/health

# API documentation
# Visit: https://your-app.railway.app/docs
```

## Step 7: Update Flutter App

Update your Flutter app to use the Railway URL:

```dart
// In your Flutter app
const String API_BASE_URL = 'https://your-app.railway.app';
```

## Default Users (After Seeding)

After running the seed script, you'll have these test users:

- **Admin User**
  - Email: `admin@fincount.com`
  - Password: `admin123`

- **Test User**
  - Email: `user@fincount.com`
  - Password: `user123`

⚠️ **IMPORTANT**: Change these passwords in production!

## Database Management

### View Database
```bash
# Connect to database via Railway CLI
railway connect postgres
```

### Run Migrations Manually
```bash
# Upgrade to latest
railway run alembic upgrade head

# Downgrade one version
railway run alembic downgrade -1

# View migration history
railway run alembic history
```

### Create New Migration
```bash
# After modifying models.py
alembic revision --autogenerate -m "Description of changes"

# Then deploy and run
railway run alembic upgrade head
```

## Troubleshooting

### Issue: Database connection fails
- Check that PostgreSQL service is running in Railway
- Verify `DATABASE_URL` environment variable is set
- Check Railway logs for connection errors

### Issue: Migrations fail
- Ensure all dependencies are installed
- Check that models are properly imported in `alembic/env.py`
- Review migration files in `alembic/versions/`

### Issue: CORS errors from Flutter
- Verify CORS middleware is configured in `main.py`
- Check that your Flutter app is using the correct API URL
- Review Railway logs for CORS-related errors

## Local Development

To test with PostgreSQL locally:

```bash
# Set DATABASE_URL environment variable
export DATABASE_URL="postgresql://user:password@localhost/fincount"

# Run migrations
alembic upgrade head

# Seed data
python seed.py

# Start server
uvicorn main:app --reload
```

## Production Checklist

- [ ] Change default user passwords
- [ ] Set custom `SECRET_KEY` environment variable
- [ ] Update CORS `allow_origins` to specific domains
- [ ] Enable Railway's automatic deployments from GitHub
- [ ] Set up monitoring and logging
- [ ] Configure custom domain (optional)
- [ ] Set up database backups in Railway

## Useful Commands

```bash
# View logs
railway logs

# Open Railway dashboard
railway open

# Check service status
railway status

# Run one-off commands
railway run <command>
```

## Support

- Railway Documentation: https://docs.railway.app
- FastAPI Documentation: https://fastapi.tiangolo.com
- Alembic Documentation: https://alembic.sqlalchemy.org

---

**Your API is now ready for production! 🚀**
