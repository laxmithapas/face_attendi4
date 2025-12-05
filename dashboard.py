import streamlit as st
import pandas as pd
import time
from datetime import datetime
from database import get_session, Person, Attendance, Encoding, get_monthly_attendance_count, delete_user, log_audit_event

# ... (setup code)

# Authentication
SESSION_TIMEOUT = 300 # 5 minutes

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'last_activity' not in st.session_state:
    st.session_state.last_activity = time.time()

# Check Timeout
if st.session_state.authenticated:
    if time.time() - st.session_state.last_activity > SESSION_TIMEOUT:
        st.session_state.authenticated = False
        st.warning("Session timed out. Please login again.")
        log_audit_event("SESSION_TIMEOUT", "User session expired")
        st.rerun()
    else:
        st.session_state.last_activity = time.time()

def check_password():
    password = st.text_input("Enter Admin Password", type="password")
    if st.button("Login"):
        if password == "admin123":
            st.session_state.authenticated = True
            st.session_state.last_activity = time.time()
            log_audit_event("LOGIN_SUCCESS", "Admin logged in")
            st.rerun()
        else:
            st.error("Incorrect Password")
            log_audit_event("LOGIN_FAILURE", "Incorrect password attempt")

# ... (rest of auth logic)

if not st.session_state.authenticated:
    check_password()
    st.stop()

# Sidebar Navigation (Only show if authenticated)
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
        st.dataframe(
            df,
            column_config={
                "Duration (min)": st.column_config.ProgressColumn(
                    "Duration (min)",
                    help="Session duration in minutes",
                    format="%.2f min",
                    min_value=0,
                    max_value=480, # 8 hours
                ),
                "Confidence": st.column_config.NumberColumn(
                    "Confidence",
                    format="%.2f"
                )
            },
            hide_index=True,
        )
        
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
        
        # Flag 0 encodings
        enc_display = f"{enc_count}"
        status = "✅ Active"
        if enc_count == 0:
            enc_display = "⚠️ 0 (Not Enrolled)"
            status = "⚠️ Pending Enrollment"
        
        user_data.append({
            "ID": user.id,
            "Name": user.name,
            "Email": user.email,
            "Status": status,
            "Encodings": enc_display,
            f"Days Present ({current_month})": days_present
        })
        
    df_users = pd.DataFrame(user_data)
    
    # Apply styling for status if possible, or just show the table
    st.dataframe(
        df_users,
        column_config={
            "Status": st.column_config.TextColumn(
                "Status",
                help="User enrollment status"
            ),
        },
        hide_index=True
    )
    
    st.divider()
    st.subheader("👤 Individual Student Profile")
    
    # Select User for detailed view
    user_names = {u.name: u.id for u in users}
    selected_user_name = st.selectbox("Select Student to View Details", ["Select a student..."] + list(user_names.keys()))
    
    if selected_user_name != "Select a student...":
        user_id = user_names[selected_user_name]
        user = session.query(Person).filter_by(id=user_id).first()
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.info(f"**Name:** {user.name}")
            st.write(f"**Email:** {user.email}")
            st.write(f"**Joined:** {user.created_at.strftime('%Y-%m-%d')}")
            
            # Fetch all attendance for this user
            user_logs = session.query(Attendance).filter_by(person_id=user_id).all()
            
            # --- NEW SUBJECT-WISE LOGIC ---
            from datetime import timedelta
            
            today = datetime.now()
            start_of_week = today - timedelta(days=today.weekday()) # Monday
            start_of_week_date = start_of_week.date()
            
            weekly_subjects = {"Mon": 0, "Tue": 0, "Wed": 0, "Thu": 0, "Fri": 0}
            days_present_week = 0
            
            # Filter for current week
            current_week_logs = [log for log in user_logs if datetime.strptime(log.date, "%Y-%m-%d").date() >= start_of_week_date]
            
            # Process daily logs
            logs_by_date = {}
            for log in current_week_logs:
                if log.date not in logs_by_date:
                    logs_by_date[log.date] = []
                logs_by_date[log.date].append(log)
                
            for date_str, logs in logs_by_date.items():
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                # Only count Mon-Fri
                if date_obj.weekday() > 4: 
                    continue
                    
                day_name = date_obj.strftime("%a")
                
                # Count subjects (Slots: 9, 10, 11, 12)
                subjects_count = 0
                slots = [9, 10, 11, 12]
                
                for slot_hour in slots:
                    # Check if any log started in this hour
                    for log in logs:
                        if log.check_in_time.hour == slot_hour:
                            subjects_count += 1
                            break
                            
                weekly_subjects[day_name] = subjects_count
                if subjects_count > 0:
                    days_present_week += 1

            # --- METRICS ---
            st.metric("Total Days Present (Current Week)", f"{days_present_week} / 5")
            
            # --- WEEKLY CHART ---
            st.write("### 📊 Weekly Subject Attendance")
            st.caption("Number of subjects attended per day (Max 4)")
            
            chart_data = pd.DataFrame({
                "Day": ["Mon", "Tue", "Wed", "Thu", "Fri"],
                "Subjects": [weekly_subjects[d] for d in ["Mon", "Tue", "Wed", "Thu", "Fri"]]
            })
            
            st.bar_chart(chart_data, x="Day", y="Subjects")
            
        st.divider()
        st.subheader("⚠️ Danger Zone")
        if st.button("🗑️ Delete User", type="primary"):
            if delete_user(user_id):
                st.success(f"User {user.name} deleted successfully!")
                log_audit_event("DELETE_USER", f"Deleted user {user.name} ({user.id})")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Failed to delete user.")

session.close()
