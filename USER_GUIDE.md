# 📖 User Guide: Face Recognition Attendance System (v2)

Welcome! This guide will help you set up and use the **Research-Driven (RetinaFace + ArcFace)** system.

---

## 🚀 Step 1: One-Time Setup

Before running the app, we need to install the SOTA "brain" (InsightFace).

1.  **Open your terminal/command prompt** in this folder.
2.  **Run the main app**:
    ```bash
    python main.py
    ```
    *(The first time you run this, it will automatically download the **buffalo_l** models. This might take a minute.)*

---

## 👤 Step 2: Enroll Yourself (Register)

Now, let's teach the system what you look like using high-precision embeddings.

1.  **Start the main app**: `python main.py`
2.  Type **`1`** and press **Enter** to select "Enroll New User".
3.  Enter your **Name** and **Email** when asked.
4.  **Look at the camera window**.
5.  Follow the instructions:
    - **Press 'c'** to capture a photo.
    - Capture **5 photos** in total (Front, Left, Right, Smile, Neutral).
    - *Tip: The new RetinaFace detector is very accurate, so you don't need perfect lighting!*
6.  Once done, it will save your **512-D ArcFace Encrypted Data** and return to the menu.

---

## 📝 Step 3: Mark Attendance

Now, let's test the "Frictionless" attendance!

1.  In the main menu, type **`2`** and press **Enter** ("Start Attendance System").
2.  A camera window will open.
3.  **Look at the camera**. You should see your name and a confidence score.
4.  **Blink your eyes** naturally.
    - The system checks for "Liveness" (blinking) to make sure you are real.
    - You will see `[BLINK]` appear on screen.
5.  The system will analyze the **Time Slot** (e.g., 9:00-10:00 AM) and mark you PRESENT for that subject automatically.
6.  Press **`q`** to stop.

---

## 📊 Step 4: View Reports (Dashboard)

1.  In the main menu, type **`3`** and press **Enter** ("Launch Admin Dashboard").
2.  This will open a web page in your browser.
3.  **Login**: Enter the admin password (default: `admin123`).
4.  **Attendance Logs**: See the exact time you checked in.
5.  **Analytics**: View the **Weekly Subject Graph** to see your attendance credits.

---

## ❓ Troubleshooting

-   **"Model not found"**: Ensure you have internet connection for the first run so InsightFace can download models.
-   **"Camera not opening"**: Check if Zoom/Teams is using it.
-   **"OpenCV Error"**: If you see a GUI error, run `pip install opencv-python`.

---

## 🧠 System Architecture & UI Explained (v2 Upgrade)

### 1. The Core Technology
*   **ArcFace (AI Model)**: We use the SOTA **InsightFace** library. It maps faces to a 512-dimensional vector space using *Additive Angular Margin Loss*, vastly superior to older FaceNet models.
*   **RetinaFace (Face Detection)**: A dense detector that works even with masks or side profiles.
*   **SQLite (Database)**: Stores encrypted biometric data.

### 2. The Attendance Interface (Camera View)
*   **Bounding Box**: Green box indicates a face is detected via **RetinaFace**.
*   **Liveness Challenge**: The system issues random commands to prove humanity.
*   **Real-Time Feedback**: Displays "Attendance Marked!" instantly upon success.

### 3. The Admin Dashboard (Analytics)
*   **Duration Bar 📊**: Visual progress bar for work hours.
*   **Weekly Subject Graph**: Shows credits earned per subject slot.
*   **Audit Logging**: Tracks every admin login for security.
