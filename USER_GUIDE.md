# 📖 User Guide: Face Recognition Attendance System

Welcome! This guide will help you set up and use the system in 3 simple steps.

## 🚀 Step 1: One-Time Setup

Before running the app, we need to install the "brain" (models) for the AI.

1.  **Open your terminal/command prompt** in this folder.
2.  **Run this command** to download the necessary AI model:
    ```bash
    python download_models.py
    ```
    *(Wait for it to say "You are ready to go!")*

---

## 👤 Step 2: Enroll Yourself (Register)

Now, let's teach the system what you look like.

1.  **Start the main app**:
    ```bash
    python main.py
    ```
2.  Type **`1`** and press **Enter** to select "Enroll New User".
3.  Enter your **Name** and **Email** when asked.
4.  **Look at the camera window**.
5.  Follow the instructions:
    - **Press 'c'** to capture a photo.
    - Capture **5 photos** in total (Front, Left, Right, Smile, Neutral).
    - *Tip: Move your head slightly for each photo so the AI learns your face better!*
6.  Once done, it will save your data and return to the menu.

---

## 📝 Step 3: Mark Attendance

Now, let's test if it recognizes you!

1.  In the main menu, type **`2`** and press **Enter** ("Start Attendance System").
2.  A camera window will open.
3.  **Look at the camera**. You should see your name and a confidence score (e.g., "John Doe (0.85)").
4.  **Blink your eyes** naturally.
    - The system checks for "Liveness" (blinking) to make sure you are real and not a photo.
    - You will see `[BLINK]` appear on screen when you blink.
5.  After a few seconds of recognizing you + blinking, it will show **"Attendance Marked!"** in Green.
6.  Press **`q`** to stop and go back to the menu.

---

## 📊 Step 4: View Reports (Dashboard)

See who has marked attendance.

1.  In the main menu, type **`3`** and press **Enter** ("Launch Admin Dashboard").
2.  This will open a web page in your browser.
3.  **Attendance Logs**: See the list of people who checked in today.
4.  **User Management**: See all registered users.
5.  You can download the report as a CSV file.

---

## ❓ Troubleshooting

-   **"Model not found"**: Make sure you ran `python download_models.py` first.
-   **"Camera not opening"**: Check if another app (like Zoom/Teams) is using your webcam.
-   **"Unknown"**: If it doesn't recognize you, try enrolling again with better lighting.
