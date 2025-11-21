import sys
import os
from database import init_db

def main():
    # Initialize Database
    init_db()
    
    while True:
        print("\n=== Face Recognition Attendance System ===")
        print("1. Enroll New User")
        print("2. Start Attendance System")
        print("3. Launch Admin Dashboard")
        print("4. Exit")
        
        choice = input("Enter choice (1-4): ")
        
        if choice == '1':
            from enrollment import enroll_user
            enroll_user()
        elif choice == '2':
            from attendance import run_attendance_system
            run_attendance_system()
        elif choice == '3':
            import subprocess
            import sys
            print("Launching Dashboard in background...")
            print("Press Enter to return to menu...")
            
            # Prepare environment variables to disable prompts
            env = os.environ.copy()
            env["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"
            env["STREAMLIT_SERVER_HEADLESS"] = "true"
            
            # Run streamlit via python -m to ensure it uses the current environment
            subprocess.Popen([sys.executable, "-m", "streamlit", "run", "dashboard.py"], 
                             shell=True, env=env)
            input() # Wait for user to press enter before showing menu again
        elif choice == '4':
            print("Exiting...")
            sys.exit()
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
