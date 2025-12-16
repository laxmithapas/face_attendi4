import os
import shutil
from config import DB_PATH, ENROLLMENT_DIR, MODELS_DIR

def reset_system():
    print("WARNING: This will delete ALL user data, embeddings, and attendance records.")
    confirm = input("Are you sure? Type 'DELETE' to confirm: ")
    
    if confirm == "DELETE":
        # Delete DB
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)
            print(f"Deleted {DB_PATH}")
            
        # Delete Images
        if os.path.exists(ENROLLMENT_DIR):
            shutil.rmtree(ENROLLMENT_DIR)
            os.makedirs(ENROLLMENT_DIR)
            print(f"Cleared {ENROLLMENT_DIR}")
            
        print("System Reset Complete. Run 'python main.py' to re-initialize.")
    else:
        print("Cancelled.")

if __name__ == "__main__":
    reset_system()
