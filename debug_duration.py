from database import get_session, Attendance, Person

def check_duration():
    session = get_session()
    try:
        # Get the user (assuming ID 1 based on previous logs, or fetch all)
        logs = session.query(Attendance).all()
        print(f"Total Logs: {len(logs)}")
        for log in logs:
            print(f"Date: {log.date}, PersonID: {log.person_id}, Duration: {log.session_duration}, In: {log.check_in_time}, Out: {log.check_out_time}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    check_duration()
