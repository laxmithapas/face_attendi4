import streamlit as st
import pandas as pd
from database import get_session, Person, Attendance, Encoding, get_monthly_attendance_count
from datetime import datetime

st.set_page_config(page_title="Attendance Dashboard", layout="wide")

st.title("Face Recognition Attendance Dashboard")

# Sidebar
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Attendance Logs", "User Management"])

session = get_session()

if page == "Attendance Logs":
    st.header("Attendance Logs")
    
    # Filters
    col1, col2 = st.columns(2)
    with col1:
        date_filter = st.date_input("Filter by Date", datetime.now())
    
    # Query
    query = session.query(Attendance).join(Person).filter(Attendance.date == str(date_filter))
    logs = query.all()
    
    data = []
    for log in logs:
        data.append({
            "ID": log.person.id,
            "Name": log.person.name,
            "Email": log.person.email,
            "Check In": log.check_in_time.strftime("%H:%M:%S"),
            "Check Out": log.check_out_time.strftime("%H:%M:%S") if log.check_out_time else "Active",
            "Duration (min)": round(log.session_duration, 2),
            "Confidence": round(log.confidence_score, 2)
        })
        
    df = pd.DataFrame(data)
    if not df.empty:
        st.dataframe(df)
        
        # Export
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            "Download CSV",
            csv,
            "attendance_logs.csv",
            "text/csv",
            key='download-csv'
        )
    else:
        st.info("No attendance records found for this date.")

elif page == "User Management":
    st.header("Registered Users")
    
    users = session.query(Person).all()
    
    user_data = []
    current_month = datetime.now().strftime("%Y-%m")
    
    for user in users:
        enc_count = session.query(Encoding).filter_by(person_id=user.id).count()
        days_present = get_monthly_attendance_count(user.id, current_month)
        
        user_data.append({
            "ID": user.id,
            "Name": user.name,
            "Email": user.email,
            "Joined": user.created_at.strftime("%Y-%m-%d"),
            "Encodings": enc_count,
            f"Days Present ({current_month})": days_present
        })
        
    df_users = pd.DataFrame(user_data)
    st.dataframe(df_users)

session.close()
