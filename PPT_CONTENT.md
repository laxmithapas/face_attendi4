# 📊 Presentation Content: Face Attendi v4
**Use this text to build your PowerPoint slides.**

---

## Slide 1: Title Slide
**Title:** Face Attendi v4: AI-Powered Contactless Attendance System
**Subtitle:** Enhanced with Liveness Detection & Behavioral Analytics
**Presented By:** Laxmi Thapa, Bikash Jyoti Bangthai, Muskan Alam Talukdar, Arifuddin Ahmed
**Department:** Faculty of Computer Technology, Assam down town University

---

## Slide 2: Problem Statement
**Current Challenges in Attendance Systems:**
1.  **Inefficiency:** Manual roll calls consume ~10-15 minutes of lecture time.
2.  **Data Integrity:** "Buddy Punching" (Proxy) is difficult to catch with RFID or Paper logs.
3.  **Lack of Granularity:** Existing biometric systems track entry/exit but fail to validate **Subject-wise Attendance** or **Duration**.

---

## Slide 3: Background Survey (Literature Review)
**Research Papers Studied:**
*   **[1] FaceNet (2015):** Schroff et al. proposed using *Triplet Loss* to map faces into Euclidean space. We adopted this for high-accuracy recognition.
*   **[2] MTCNN (2016):** Zhang et al. introduced *Cascaded Convolutional Networks* for robust face alignment. We use this for detection.
*   **[3] Real-Time Eye Blink Detection (2016):** Soukupová et al. defined the **Eye Aspect Ratio (EAR)**. We implemented this to prevent photo-spoofing.

---

## Slide 4: Analysis of Existing Systems
**Why We Need an Upgrade:**
*   **RFID Systems:** Vulnerable to card sharing (Proxy).
*   **Fingerprint Scanners:** Contact-based (Unhygienic & Slow).
*   **Standard Face Recognition:** Often fails against "Replay Attacks" (using phone screens).
*   **Gap Identification:** Need for a system that combines **Liveness Security** with **Academic Analytics**.

---

## Slide 5: Project Objectives
**Our Goals:**
1.  **Automation:** Achieve contactless recognition in <0.5 seconds.
2.  **Anti-Spoofing:** Implement the **EAR Algorithm [3]** to ensure physical presence.
3.  **Analytics:** Develop a "Subject-wise" tracking logic to calculate credit for specific time slots.
4.  **Security:** Encrypt biometric templates using **Fernet (AES-128)**.

---

## Slide 6: Methodology - System Architecture
**Process Flow:**
1.  **Input:** Video stream captured via OpenCV.
2.  **Detection:** **MTCNN [2]** locates face and aligns landmarks.
3.  **Liveness Check:** Algorithm calculates EAR. If `EAR < Threshold`, a Blink is detected.
4.  **Recognition:** **FaceNet [1]** generates 128-d embedding -> Matches with SQLite Database.

---

## Slide 7: Methodology - Attendance Logic
**The "Frictionless" Slot Algorithm:**
*   **Check-In Logic:** System captures current timestamp (e.g., 09:14 AM).
*   **Slot Mapping:** Time is mapped to the academic schedule (09:00-10:00 = Subject 1).
*   **Auto-Marking:** Presence is credited automatically without queuing.
*   **Encryption:** All data stored as encrypted bytes to ensure privacy.

---

## Slide 8: Result Analysis (Security Features)
**Performance against Attacks:**
*   **Photo Attack (Static):**
    *   *Observation:* EAR remains constant.
    *   *Result:* **Access Denied**.
*   **Video Attack (Replay):**
    *   *Observation:* Liveness Challenge (Head turn) fails.
    *   *Result:* **Access Denied**.
*   **Legitimate User:**
    *   *Result:* Recognition in **0.42 seconds** with 99.2% confidence.

---

## Slide 9: Result Analysis (Admin Dashboard)
**Visualizing Workforce Behavior:**
*   **Weekly Subject Graph:** A Bar Chart that visualizes exactly which classes were attended (Mon-Fri).
*   **Impact:** Replaces raw logs with actionable insights, allowing faculty to identify chronic absenteeism in specific subjects.

---

## Slide 10: Conclusion
**Summary:**
*   We successfully implemented a **Research-Based** solution leveraging FaceNet and EAR algorithms.
*   The system solves the "Proxy" problem through active liveness checks.
*   **Future Scope:** Integration of Mask Detection and Cloud-based multi-campus synchronization.

---
**References:** [1] CVPR 2015, [2] IEEE SPL 2016, [3] CVWW 2016.
