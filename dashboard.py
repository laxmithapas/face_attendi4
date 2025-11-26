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
            
            # Calculate stats
            total_days = len(set(log.date for log in user_logs))
            avg_duration = 0
            late_count = 0
            early_leave_count = 0
            
            if user_logs:
                avg_duration = sum(log.session_duration for log in user_logs) / len(user_logs)
                
                # Late/Early Logic (Assuming 9:00 AM - 5:00 PM)
                # Late > 9:15 AM
                # Early < 4:45 PM
                for log in user_logs:
                    try:
                        check_in_time = log.check_in_time.time()
                        if check_in_time > datetime.strptime("09:15", "%H:%M").time():
                            late_count += 1
                            
                        if log.check_out_time:
                            check_out_time = log.check_out_time.time()
                            if check_out_time < datetime.strptime("16:45", "%H:%M").time():
                                early_leave_count += 1
                    except Exception:
                        pass
            
            st.metric("Total Days Present", total_days)
            st.metric("Avg. Session Duration", f"{avg_duration:.1f} min")
            
            # Punctuality Score
            punctuality_score = 0
            if total_days > 0:
                punctuality_score = ((total_days - late_count) / total_days) * 100
            
            st.metric("Punctuality Score", f"{punctuality_score:.1f}%", delta=f"{punctuality_score:.1f}%", delta_color="normal" if punctuality_score >= 80 else "inverse")
            
            # Late/Early Stats
            # Late/Early/On-Time Stats
            on_time_count = total_days - late_count
            
            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric("On Time", on_time_count, delta=on_time_count, delta_color="normal", help="Arrived before 9:15 AM")
            with c2:
                st.metric("Late (>9:15)", late_count, delta=late_count, delta_color="inverse", help="Arrived after 9:15 AM")
            with c3:
                st.metric("Early (<4:45)", early_leave_count, delta=early_leave_count, delta_color="inverse", help="Left before 4:45 PM")

        with col2:
            st.write("### 📅 Monthly Attendance Calendar")
            
            # Month Selection for Calendar
            # Generate last 12 months
            available_months = []
            for i in range(12):
                d = datetime.now() - pd.DateOffset(months=i)
                available_months.append(d.strftime("%Y-%m"))
            
            # Use a unique key to avoid conflict with other selectboxes
            cal_month_str = st.selectbox("Select Month", available_months, key="calendar_month_select")
            
            # Parse selected month
            year, month = map(int, cal_month_str.split('-'))
            
            # Simple Calendar Grid
            import calendar
            
            # Get present dates
            present_dates = {log.date for log in user_logs}
            
            cal = calendar.monthcalendar(year, month)
            month_name = calendar.month_name[month]
            
            st.write(f"**{month_name} {year}**")
            
            # Create a visual grid using columns
            cols = st.columns(7)
            days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
            for i, day in enumerate(days):
                cols[i].write(f"**{day}**")
            
            for week in cal:
                cols = st.columns(7)
                for i, day in enumerate(week):
                    if day == 0:
                        cols[i].write("")
                    else:
                        date_str = f"{year}-{month:02d}-{day:02d}"
                        if date_str in present_dates:
                            cols[i].success(f"{day}") # Green for present
                        else:
                            # Check if it's a past weekday (Absent)
                            is_weekend = i >= 5
                            current_date_str = datetime.now().strftime("%Y-%m-%d")
                            if date_str < current_date_str and not is_weekend:
                                cols[i].error(f"{day}") # Red for absent
                            else:
                                cols[i].write(f"{day}") # Grey for future/weekend

        # Charts with Month Filter and Width Adjustment
        st.write("### 📈 Attendance Trends")
        
        if user_logs:
            # Month Filter
            all_months = sorted(list(set(log.date[:7] for log in user_logs)), reverse=True)
            # Add "All Time" option
            filter_options = ["All Time"] + all_months
            
            selected_month = st.selectbox("Filter Trends by Month", filter_options)
            
            # Filter data
            chart_data = []
            for log in user_logs:
                if selected_month == "All Time" or log.date.startswith(selected_month):
                    # Ensure minimum visibility for 0 duration
                    duration = log.session_duration
                    if duration == 0:
                        duration = 0.5 # Small bar to show "Present"
                    
                    chart_data.append({
                        "Date": log.date,
                        "Duration (min)": duration
                    })
            
            df_chart = pd.DataFrame(chart_data)
            
            # Layout adjustment (Narrower chart)
            c_chart, c_empty = st.columns([3, 1]) # 75% width
            with c_chart:
                if not df_chart.empty:
                    st.bar_chart(df_chart, x="Date", y="Duration (min)")
                else:
                    st.info(f"No data for {selected_month}")
        else:
            st.info("No attendance data available for charts.")

session.close()
