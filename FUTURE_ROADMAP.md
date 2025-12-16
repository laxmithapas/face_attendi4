# 🚀 Future Roadmap: Evolution from Baseline to SOTA

This document outlines the strategic upgrade path for **Face Attendi v4**. It contrasts our current "Classical Baseline" with modern "State-of-the-Art" (SOTA) methods, demonstrating our academic awareness of the field's evolution.

---

## 1. Face Detection: The Pivot to Single-Stage Detectors

| Feature | Current Baseline (Face Attendi v4) | SOTA Upgrade (v5 Target) |
| :--- | :--- | :--- |
| **Model** | **MTCNN** (Multi-task Cascaded CNN) [2016] | **RetinaFace** (Single-stage Dense Detector) [2020] |
| **Architecture** | 3-Stage Cascade (P-Net -> R-Net -> O-Net) | Single-stage with Feature Pyramid Networks (FPN) |
| **Pros** | Lightweight, easy to interpret, good for frontal faces. | Validated on WIDER FACE dataset. Handles extreme occlusion and tiny faces much better. |
| **Why Change?** | MTCNN struggles with side profiles and heavy occlusion compared to modern dense detectors. |

> **Viva Defense:** "We used MTCNN as a reliable, lightweight baseline to establish our end-to-end pipeline. For v5, we have identified RetinaFace as the optimal upgrade to handle crowded or occluded scenarios."

---

## 2. Face Recognition: From Triplet Loss to Angular Margin

| Feature | Current Baseline (Face Attendi v4) | SOTA Upgrade (v5 Target) |
| :--- | :--- | :--- |
| **Model** | **FaceNet** (Inception ResNet v1) [2015] | **ArcFace / InsightFace** (ResNet-100) [2019] |
| **Loss Function** | Triplet Loss (Euclidean Distance) | Additive Angular Margin Loss (Geodesic Distance) |
| **Pros** | Proven industry standard, excellent documentation. | Maximizes class separability on hypersphere. Better discrimination for large-scale datasets (MS-Celeb-1M). |
| **Why Change?** | Triplet mining can be unstable during training. | Margin-based losses provide sharper decision boundaries between similar-looking identities. |

> **Viva Defense:** "FaceNet provided a strong foundation for our prototype. However, we acknowledge that ArcFace's angular margin loss offers superior discriminative power, which is our next step for scaling the system."

---

## 3. Liveness Detection: Beyond Geometric Heuristics

| Feature | Current Baseline (Face Attendi v4) | SOTA Upgrade (v5 Target) |
| :--- | :--- | :--- |
| **Method** | **EAR Optimization** (Geometric Layout) [2016] | **Deep FAS** (Face Anti-Spoofing) [2023] |
| **Logic** | Calculates Eye Aspect Ratio from landmarks. | CNN/Transformer analyzing texture (rPPG, Moiré patterns). |
| **Pros** | Extremely fast, explainable, no training data needed. | Robust against high-quality video replay attacks. |
| **Cons** | Can be fooled by high-frame-rate video replays. | Requires heavy computation and large diverse datasets. |

> **Viva Defense:** "EAR is an excellent 'first line of defense' due to its speed. A production-grade system would combine EAR with a secondary Deep-FAS network to analyze texture cues for definitive spoof detection."

---

## 4. Summary of Evolution

*   **v4 (Current):** Focuses on **System Integration**, **Behavioral Analytics**, and **Baseline Security** using classical, interpretable models.
*   **v5 (Planned):** Will focus on **Model Robustness** by swapping the backbone components (RetinaFace + ArcFace) while keeping the Logic/Analytics modules intact.
