"""
FastAPI Main Application
This is the entry point for the Fincount API backend
"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import uvicorn

# Import routers
import router_auth
import router_batches
import router_sessions

# Import database initialization
from database import init_db

app = FastAPI(
    title="Fincount API",
    description="Backend API for Fincount Flutter Application",
    version="1.0.0"
)

# CORS Configuration - allows Flutter app to communicate with API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your Flutter app's domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database tables on startup
@app.on_event("startup")
async def startup_event():
    """Create database tables on startup"""
    init_db()
    port = os.environ.get("PORT", "8000")
    print("✅ Database initialized successfully")
    print(f"🚀 Server is running on port {port}")
    print(f" API Documentation at /docs")

# Include routers
app.include_router(router_auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(router_batches.router, prefix="/api/batches", tags=["Batches"])
app.include_router(router_sessions.router, prefix="/api/sessions", tags=["Sessions"])

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Fincount API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/api/health")
async def health_check():
    """Health check endpoint - used by Flutter app to verify connection"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }

if __name__ == "__main__":
    # Run the server
    # Railway provides PORT via environment variable
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",  # Allows external connections
        port=port,  # Use Railway's dynamic PORT
        reload=True  # Auto-reload on code changes (development only)
    )
