"""Reset database tables with updated schema."""
import sys
from app.database import engine, Base
from app.models import User, Function, Component, Dashboard

def reset_database():
    """Drop all tables and recreate them."""
    print("Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    print("✓ Tables dropped")

    print("Creating tables with new schema...")
    Base.metadata.create_all(bind=engine)
    print("✓ Tables created")

    print("\nDatabase reset complete!")
    print("Tables created:")
    for table in Base.metadata.tables.keys():
        print(f"  - {table}")

if __name__ == "__main__":
    try:
        reset_database()
    except Exception as e:
        print(f"Error resetting database: {e}", file=sys.stderr)
        sys.exit(1)
