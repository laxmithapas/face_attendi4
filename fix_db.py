from database import engine
from sqlalchemy import text

def fix_database():
    print("Attempting to fix database schema...")
    try:
        with engine.connect() as conn:
            conn.execute(text("ALTER TABLE attendance ADD COLUMN liveness_verified BOOLEAN DEFAULT 0"))
            print("SUCCESS: Added 'liveness_verified' column.")
    except Exception as e:
        print(f"INFO: Column might already exist or error occurred: {e}")

if __name__ == "__main__":
    fix_database()
