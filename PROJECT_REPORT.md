# 📑 PROJECT REPORT: Face Recognition Attendance System with Behavioral Analytics

**Project Name:** Face Attendi v4
**Domain:** Computer Vision / Biometrics / Data Analytics
**Technology Stack:** Python, OpenCV, FaceNet, Streamlit, SQLite

---

## 1. 📝 Abstract

This project aims to modernize traditional attendance systems by leveraging **Face Recognition** and **Behavioral Analytics**. Unlike simple biometric counters, this system focuses on **Data Integrity** (Anti-Spoofing) and **Workforce Discipline** (Duration Tracking). It provides a contactless, secure, and insightful solution for educational and corporate environments.

---

## 2. 🎯 Objectives

1.  **Automate Attendance:** Eliminate manual roll calls and paper sheets.
2.  **Ensure Security:** Prevent "Buddy Punching" using Liveness Detection (Blink Check).
3.  **Track Discipline:** Monitor "Time-in-Office" to identify late arrivals and early departures.
4.  **Provide Insights:** Visualise attendance patterns using Heatmaps and Trend Charts.

---

## 3. 🏗️ System Architecture

The system is composed of three main modules:

### A. The Vision Module (The "Eyes")
*   **Face Detection (MTCNN):** Locates faces in the video feed, robust against lighting changes.
*   **Face Recognition (FaceNet):** Converts face images into 128-dimensional numerical vectors ("Encodings").
*   **Liveness Detection (EAR):** Calculates the **Eye Aspect Ratio** to detect blinking, ensuring the subject is a live human.

### B. The Logic Module (The "Brain")
*   **Enrollment:** Captures 5 angles of a user's face to create a robust profile.
*   **Identification:** Compares live video encodings with the database using Euclidean distance.
*   **Session Logic:**
    *   **Check-In:** First sighting of the day.
    *   **Check-Out:** Last sighting of the day (continuously updated).

### C. The Analytics Module (The "Dashboard")
*   **Database (SQLite):** Stores User Profiles, Encodings, and Attendance Logs.
*   **Dashboard (Streamlit):** A web-based interface for administrators.

---

## 4. 🚀 Key Features Implemented

### 1. Robust Biometric Security
*   **Anti-Spoofing:** The system rejects photos or videos displayed on screens by requiring a natural blink.
*   **Confidence Scores:** Every attendance record includes a confidence percentage (e.g., 98% match), creating an audit trail.

### 2. Smart Attendance Logging
*   **Auto-Duration Calculation:** The system automatically calculates the total hours spent on campus/office.
*   **Zero-Touch Operation:** Users simply walk past the camera; no buttons needed.

### 3. Advanced Admin Dashboard (Analytics)
*   **Real-Time Logs:** View live check-ins with "Duration Bars" indicating work progress.
*   **Student Profiles:** Dedicated pages for each user showing their specific history.
*   **Calendar Heatmap:** A visual grid (Green/Red) showing monthly attendance at a glance.
*   **Discipline Stats:** Automatic counters for **Late Arrivals** (>9:15 AM) and **Early Departures** (<4:45 PM).
*   **Trend Analysis:** Bar charts visualizing attendance consistency over time (filterable by Month or All Time).

### 4. Data Integrity Checks
*   **Enrollment Validation:** The dashboard flags users with "0 Encodings" as **Pending Enrollment**, preventing "Ghost Users" who exist in the database but cannot be recognized.

---

## 5. 💻 Technical Implementation Details

### Database Schema
*   **Table `persons`**: Stores Name, Email, Join Date.
*   **Table `encodings`**: Stores the 128-d vector blobs and reference image paths.
*   **Table `attendance`**: Stores Date, Check-In, Check-Out, Confidence Score, and Session Duration.

### Algorithms Used
*   **FaceNet (Inception ResNet v1):** Pre-trained on VGGFace2 dataset for state-of-the-art accuracy.
*   **Euclidean Distance:** Used to measure similarity between faces (Lower distance = Higher match).

---

## 6. 📊 Results & Performance

*   **Accuracy:** The system achieves high accuracy (>99%) on enrolled users.
*   **Speed:** Recognition occurs in near real-time (~0.5 seconds per frame).
*   **Usability:** The Streamlit dashboard allows non-technical administrators to manage thousands of records effortlessly.

---

## 7. 🏁 Conclusion

The **Face Recognition Attendance System** successfully bridges the gap between simple attendance logging and actionable workforce analytics. By combining **Liveness Detection** for security with **Visual Analytics** for management, it offers a complete "A to Z" solution for modern attendance needs.

---

**Developed by:** [Your Name/Team]
**Date:** November 2025
