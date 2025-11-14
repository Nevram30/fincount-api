"""
Seed script to populate initial user data
Run this script to create a default admin user for testing
"""
import os
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import User
from auth import get_password_hash

def seed_users():
    """Create initial users for the application"""
    db = SessionLocal()
    
    try:
        # Check if users already exist
        existing_users = db.query(User).count()
        if existing_users > 0:
            print(f"⚠️  Database already has {existing_users} user(s). Skipping seed.")
            return
        
        # Create default admin user
        admin_user = User(
            email="admin@fincount.com",
            name="Admin User",
            hashed_password=get_password_hash("admin123"),
            role="admin"
        )
        
        # Create default test user
        test_user = User(
            email="user@fincount.com",
            name="Test User",
            hashed_password=get_password_hash("user123"),
            role="user"
        )
        
        db.add(admin_user)
        db.add(test_user)
        db.commit()
        
        print("✅ Successfully seeded database with initial users:")
        print(f"   - Admin: admin@fincount.com / admin123")
        print(f"   - User: user@fincount.com / user123")
        print("\n⚠️  IMPORTANT: Change these passwords in production!")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


def main():
    """Main function to run migrations and seed data"""
    print("🌱 Starting database seed process...")
    print(f"📊 Database URL: {os.getenv('DATABASE_URL', 'sqlite:///./fincount.db')}")
    
    # Create tables if they don't exist
    print("\n📋 Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully")
    
    # Seed users
    print("\n👤 Seeding users...")
    seed_users()
    
    print("\n🎉 Database seed completed!")


if __name__ == "__main__":
    main()
