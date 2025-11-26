# 🧠 Deep Dive: How the Attendance & Scoring System Works

This document explains the exact logic behind every number, color, and score you see on the dashboard. It covers all possible scenarios to help you understand how the system judges "Discipline".

---

## 1. The Core Rules (The "Law")

The system operates on a fixed schedule to decide if someone is "Good" or "Bad".

| Event | Time Threshold | Meaning |
| :--- | :--- | :--- |
| **Office Start Time** | **9:00 AM** | The official start of the day. |
| **Late Threshold** | **9:15 AM** | If you arrive *after* this, you are marked **LATE**. |
| **Early Leave Threshold** | **4:45 PM** | If you leave *before* this, you are marked **EARLY DEPARTURE**. |
| **Office End Time** | **5:00 PM** | The official end of the day. |

---

## 2. The "Punctuality Score" Formula 🧮

This score tells you: *"What percentage of days was this person on time?"*

$$ \text{Score} = \left( \frac{\text{Total Days Present} - \text{Late Days}}{\text{Total Days Present}} \right) \times 100 $$

*   **🟢 Green Score:** 80% - 100% (Excellent Discipline)
*   **🔴 Red Score:** 0% - 79% (Needs Improvement)

---

## 3. Detailed Scenarios (Examples)

Let's look at 4 different employees to see how the math works in real life.

### 👤 Scenario A: The "Perfect" Employee (Alice)
Alice is extremely disciplined. She always comes on time.

*   **Day 1:** Arrived 8:55 AM (On Time)
*   **Day 2:** Arrived 9:00 AM (On Time)
*   **Day 3:** Arrived 9:10 AM (On Time)
*   **Day 4:** Arrived 8:45 AM (On Time)

**The Math:**
*   Total Days: 4
*   Late Days: 0
*   Calculation: `(4 - 0) / 4 = 1.0` -> **100%**

**Dashboard Result:**
*   **Punctuality:** **100%** 🟢
*   **Late Arrivals:** 0
*   **On Time:** 4 🟢

---

### 👤 Scenario B: The "Sometimes Late" Employee (Bob)
Bob tries his best but overslept once.

*   **Day 1:** Arrived 9:00 AM (On Time)
*   **Day 2:** Arrived **9:30 AM** (LATE! 🔴)
*   **Day 3:** Arrived 9:05 AM (On Time)
*   **Day 4:** Arrived 9:14 AM (On Time)

**The Math:**
*   Total Days: 4
*   Late Days: 1
*   Calculation: `(4 - 1) / 4 = 0.75` -> **75%**

**Dashboard Result:**
*   **Punctuality:** **75%** 🔴 (Warning!)
*   **Late Arrivals:** 1 🔴
*   **On Time:** 3 🟢

---

### 👤 Scenario C: The "Habitual Latecomer" (Charlie)
Charlie doesn't care about rules. He is almost always late.

*   **Day 1:** Arrived **10:00 AM** (LATE! 🔴)
*   **Day 2:** Arrived **9:45 AM** (LATE! 🔴)
*   **Day 3:** Arrived **9:20 AM** (LATE! 🔴)
*   **Day 4:** Arrived 9:00 AM (On Time - Finally!)

**The Math:**
*   Total Days: 4
*   Late Days: 3
*   Calculation: `(4 - 3) / 4 = 0.25` -> **25%**

**Dashboard Result:**
*   **Punctuality:** **25%** 🔴 (Critical!)
*   **Late Arrivals:** 3 🔴
*   **On Time:** 1 🟢

---

### 👤 Scenario D: The "Early Leaver" (Dave)
Dave comes on time, but he sneaks out early.
*Note: Leaving early does NOT affect the Punctuality Score (which is about arrival), but it triggers a separate "Early Departure" flag.*

*   **Arrival:** 9:00 AM (On Time)
*   **Departure:** **3:30 PM** (EARLY! 🔴)

**Dashboard Result:**
*   **Punctuality:** **100%** 🟢 (He arrived on time!)
*   **Early Departures:** 1 🔴 (But he left early)

---

## 4. How "Session Duration" is Calculated ⏱️

The system is smart. It doesn't just check you once. It watches you all day.

1.  **Check-In:** The **First Time** the camera sees you today (e.g., 9:00 AM).
2.  **Check-Out:** The **Last Time** the camera saw you today (e.g., 5:00 PM).
3.  **Duration:** `Check-Out - Check-In`

**Example:**
*   Camera sees Alice at **9:00 AM** (Check-In starts).
*   Camera sees Alice at **12:00 PM** (Lunch).
*   Camera sees Alice at **5:00 PM** (Last sighting).
*   **Total Duration:** 9:00 AM to 5:00 PM = **8 Hours**.

**What if I forget to check out?**
*   If the camera only sees you ONCE at 9:00 AM and never again:
*   Duration = 0 minutes.
*   The Dashboard will show a tiny bar to indicate "Present but Unknown Duration".

---

## 5. Summary Table

| Metric | Good Behavior (Green 🟢) | Bad Behavior (Red 🔴) |
| :--- | :--- | :--- |
| **On Time** | Arriving **before 9:15 AM** | N/A |
| **Late Arrival** | N/A | Arriving **after 9:15 AM** |
| **Early Departure**| Leaving **after 4:45 PM** | Leaving **before 4:45 PM** |
| **Punctuality** | Score **80% - 100%** | Score **0% - 79%** |

This logic ensures that the system is **Fair**, **Transparent**, and **Automated**. No human bias involved!
