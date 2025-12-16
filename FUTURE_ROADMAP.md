# 🚀 Future Roadmap: Development Trajectory

This document outlines the evolutionary path of **Face Attendi**. We have successfully transitioned from a Classical Baseline (v1) to a State-of-the-Art Research System (v2).

---

## 1. Phase 1: The Baseline (v1) - *COMPLETED*
*   **Detection:** MTCNN (Multi-task Cascaded CNN).
*   **Recognition:** FaceNet (Triplet Loss).
*   **Liveness:** Simple Blink check.
*   **Result:** A working prototype demonstrating the concept of "Frictionless Attendance".

---

## 2. Phase 2: The SOTA Upgrade (v2) - *CURRENT STATUS* 📍
**We have successfully implemented detailed research upgrades to meet 2024/2025 academic standards.**

| Feature | SOTA Implementation | Research Backing |
| :--- | :--- | :--- |
| **Detection** | **RetinaFace** (ResNet50) | *Deng et al., CVPR 2020* - Handles masks & occlusion. |
| **Recognition** | **ArcFace** (Angular Margin) | *Deng et al., CVPR 2019* - Hypersphere embedding space. |
| **Matching** | **Cosine Similarity** | Mathematically superior to Euclidean distance for high-dimensional vectors. |
| **Analytics** | **Weekly Subject Graph** | Focuses on subject-wise attendance credits. |

> **Viva Defense:** "We did not just stick to 2015-era tutorials. We refactored the entire core engine to use InsightFace (RetinaFace + ArcFace) to align with current Computer Vision research."

---

## 3. Phase 3: The Enterprise Scale (Future Goals v3)
Now that the core engine is robust, future work will focus on **Scale** and **Accessibility**.

### A. Deep Anti-Spoofing (Deep FAS)
*   **Current:** EAR (Blink) + Geometric Checks.
*   **Future:** Implement a **Texture-based CNN** (e.g., MiniFASNet) to detect "Moiré patterns" from screen replays.
    *   *Reference:* Yu et al., "Deep Learning for Face Anti-Spoofing: A Survey" (IEEE 2023).

### B. Mobile Integration
*   **Plan:** Develop a **Flutter/React Native App** for students to view their own attendance graphs on their phones.
*   **Backend:** Expose `main.py` logic via a **FastAPI** REST interface.

### C. Cloud Deployment
*   **Plan:** Containerize the application using **Docker**.
*   **Target:** Deploy to AWS/GCP with a managed PostgreSQL database for handling 10,000+ users.

---
