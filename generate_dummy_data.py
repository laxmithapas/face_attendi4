import random
from datetime import datetime, timedelta
from database import get_session, Person, Attendance

def generate_data():
    session = get_session()
    users = session.query(Person).all()
    
    if not users:
        print("No users found! Please enroll a user first.")
        return

    print(f"Found {len(users)} users. Generating data for the last 7 days...")
    
    # Slots: 9-10, 10-11, 11-12, 12-1
    slots = [9, 10, 11, 12]
    
    today = datetime.now()
    
    for i in range(7): # Last 7 days
        current_date = today - timedelta(days=i)
        
        # Skip weekends
        if current_date.weekday() > 4:
            continue
            
        date_str = current_date.strftime("%Y-%m-%d")
        print(f"Processing {date_str}...")
        
        for user in users:
            # Randomly decide if student is present today (90% chance)
            if random.random() > 0.1:
                # Randomly decide how many subjects they attended (1 to 4)
                # Weights: mostly 4, sometimes 3, rarely 1-2
                num_subjects = random.choices([1, 2, 3, 4], weights=[5, 10, 20, 65])[0]
                
                # Pick random slots
                attended_slots = sorted(random.sample(slots, num_subjects))
                
                for hour in attended_slots:
                    # Generate Check-in (e.g., 9:00 - 9:10)
                    check_in_min = random.randint(0, 10)
                    check_in_time = current_date.replace(hour=hour, minute=check_in_min, second=0)
                    
                    # Generate Check-out (e.g., 9:50 - 9:59)
                    check_out_min = random.randint(50, 59)
                    check_out_time = current_date.replace(hour=hour, minute=check_out_min, second=0)
                    
                    duration = (check_out_time - check_in_time).total_seconds() / 60.0
                    
                    # Create Record
                    att = Attendance(
                        person_id=user.id,
                        date=date_str,
                        check_in_time=check_in_time,
                        check_out_time=check_out_time,
                        confidence_score=random.uniform(0.75, 0.95),
                        session_duration=duration
                    )
                    session.add(att)
                    
    session.commit()
    print("✅ Dummy data generated successfully!")
    session.close()

if __name__ == "__main__":
    generate_data()
