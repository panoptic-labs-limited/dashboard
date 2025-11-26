"""Create test user for development."""
import sys
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_test_user():
    """Create testuser account."""
    db = SessionLocal()
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(User.username == "testuser").first()
        if existing_user:
            print("✓ Test user already exists")
            return

        # Create new user
        hashed_password = pwd_context.hash("testpassword123")
        user = User(
            username="testuser",
            email="test@example.com",
            hashed_password=hashed_password
        )
        db.add(user)
        db.commit()
        print("✓ Test user created successfully")
        print(f"  Username: testuser")
        print(f"  Password: testpassword123")

    except Exception as e:
        print(f"Error creating test user: {e}", file=sys.stderr)
        db.rollback()
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    create_test_user()
