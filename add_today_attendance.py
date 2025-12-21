from datetime import datetime
from database import get_session, Person, Attendance
import random

def add_today_data():
    session = get_session()
    users = session.query(Person).all()
    
    if not users:
        print("No users found in database.")
        return

    today_str = datetime.now().strftime("%Y-%m-%d")
    print(f"Adding dummy data for Date: {today_str}")

    count = 0
    for user in users:
        # Check if already exists for today to avoid duplicates
        exists = session.query(Attendance).filter_by(person_id=user.id, date=today_str).first()
        if exists:
            print(f"Skipping {user.name} (Already present today)")
            continue

        # Create entry for 10 AM slot (realistic for morning attendance)
        # Check-in: 10:05 AM
        check_in = datetime.now().replace(hour=10, minute=random.randint(0, 5), second=0)
        # Check-out: 10:55 AM
        check_out = datetime.now().replace(hour=10, minute=random.randint(50, 55), second=0)
        
        duration = (check_out - check_in).total_seconds() / 60.0
        
        att = Attendance(
            person_id=user.id,
            date=today_str,
            check_in_time=check_in,
            check_out_time=check_out,
            confidence_score=random.uniform(0.95, 0.99),
            session_duration=duration
        )
        session.add(att)
        print(f"✅ Marked Present: {user.name} (10:00 AM Slot)")
        count += 1

    session.commit()
    session.close()
    print(f"Successfully added {count} records for today.")

if __name__ == "__main__":
    add_today_data()
