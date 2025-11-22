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
            status = "❌ Inactive"
        
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
            
            # Late/Early Stats
            c1, c2 = st.columns(2)
            with c1:
                st.metric("Late Arrivals (>9:15)", late_count, delta=-late_count if late_count > 0 else None, delta_color="inverse")
            with c2:
                st.metric("Early Departures (<4:45)", early_leave_count, delta=-early_leave_count if early_leave_count > 0 else None, delta_color="inverse")

        with col2:
            st.write("### 📅 Monthly Attendance Calendar")
            # ... (Calendar code remains same) ...
            # Simple Calendar Grid
            import calendar
            now = datetime.now()
            year = now.year
            month = now.month
            
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
                            current_date_str = now.strftime("%Y-%m-%d")
                            if date_str < current_date_str and not is_weekend:
                                cols[i].error(f"{day}") # Red for absent
                            else:
                                cols[i].write(f"{day}") # Grey for future/weekend

        # Charts with Month Filter and Width Adjustment
        st.write("### 📈 Attendance Trends")
        
        if user_logs:
            # Month Filter
            all_months = sorted(list(set(log.date[:7] for log in user_logs)), reverse=True)
            if not all_months:
                all_months = [datetime.now().strftime("%Y-%m")]
                
            selected_month = st.selectbox("Filter Trends by Month", all_months)
            
            # Filter data
            chart_data = []
            for log in user_logs:
                if log.date.startswith(selected_month):
                    chart_data.append({
                        "Date": log.date,
                        "Duration (min)": log.session_duration
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
