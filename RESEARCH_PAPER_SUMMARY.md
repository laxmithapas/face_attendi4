# 📚 Face Attendi: Research Compendium (v1 & v2)

This document summarizes the **7 Research Papers** reviewed during the development of Face Attendi. It tracks the evolution from the initial baseline (v1) to the current SOTA implementation (v2).

---

## 🏛️ Phase 1: The Baseline (v1 Legacy)
*These papers formed the foundation of our initial prototype but were eventually replaced due to performance limitations.*

### 1. FaceNet: A Unified Embedding for Face Recognition
*   **Year:** 2015
*   **Authors:** Schroff et al. (Google)
*   **Key Finding:** Introduced **Triplet Loss**, which pulls matching faces closer and pushes different faces apart in Euclidean space. It proved that mapping faces to a 128-D vector is better than traditional "Eigenfaces".
*   **Our Usage:** Used in v1 for recognition. **Replaced in v2** because Triplet Loss is slow to converge and less accurate than ArcFace.
*   **Source:** [https://arxiv.org/abs/1503.03832](https://arxiv.org/abs/1503.03832)

### 2. Multi-task Cascaded Convolutional Networks (MTCNN)
*   **Year:** 2016
*   **Authors:** Zhang et al.
*   **Key Finding:** Proposed a 3-stage Cascade structure (P-Net, R-Net, O-Net) for face detection. It was the standard for years.
*   **Our Usage:** Used in v1 for detection. **Replaced in v2** because it struggles with side profiles and masks compared to RetinaFace.
*   **Source:** [https://arxiv.org/abs/1604.02878](https://arxiv.org/abs/1604.02878)

---

## 🚀 Phase 2: The SOTA Upgrade (v2 Production)
*These papers are CURRENTLY RUNNING in the valid codebase.*

### 3. RetinaFace: Single-shot Multi-level Face Localisation
*   **Year:** 2020
*   **Authors:** Deng et al. (InsightFace)
*   **Key Finding:** Introduced **Feature Pyramid Networks (FPN)** and pixel-wise supervision. It is far more robust than MTCNN, capable of detecting "Tiny Faces" in a crowded classroom.
*   **Our Usage:** **Implemented** in `face_detection.py`. It is our current Detection Engine.
*   **Source:** [https://arxiv.org/abs/1905.00641](https://arxiv.org/abs/1905.00641)

### 4. ArcFace: Additive Angular Margin Loss
*   **Year:** 2019
*   **Authors:** Deng et al. (InsightFace)
*   **Key Finding:** Improved upon FaceNet by using **Geodesic Distance** on a hypersphere instead of Euclidean distance. This maximizes the decision boundary between classes, making it ideal for large-scale recognition (~99.8% accuracy).
*   **Our Usage:** **Implemented** in `face_recognition.py`. It is our current Recognition Engine (512-D vectors).
*   **Source:** [https://arxiv.org/abs/1801.07698](https://arxiv.org/abs/1801.07698)

### 5. Real-Time Eye Blink Detection using Facial Landmarks (EAR)
*   **Year:** 2016
*   **Authors:** Soukupová & Čech
*   **Key Finding:** Demonstrated that the **Eye Aspect Ratio (EAR)** is a distinct geometric feature that drops strictly during a blink. It is computationally "free" compared to training a neural network for liveness.
*   **Our Usage:** **Retained from v1**. It remains in `liveness_detection.py` as our primary Anti-Spoofing check.
*   **Source:** [https://vision.fe.uni-lj.si/cvww2016/proceedings/papers/05.pdf](https://vision.fe.uni-lj.si/cvww2016/proceedings/papers/05.pdf)

---

## 🔬 Phase 3: The Research Evaluation (Studied but Not Deployed)
*These papers were reviewed for "Literature Review" and "Future Scope" but rejected for the current build.*

### 6. AdaFace: Quality Adaptive Margin for Face Recognition
*   **Year:** 2022
*   **Authors:** Kim et al.
*   **Key Finding:** Proposed a loss function that adapts the margin based on image quality (blurry vs clear). Great for CCTV enforcement.
*   **Status:** **Studied**. We acknowledge it in our PPT as "Advanced Tech", but chose ArcFace for its proven stability on CPUs.
*   **Source:** [https://arxiv.org/abs/2204.00964](https://arxiv.org/abs/2204.00964)

### 7. Deep Learning for Face Anti-Spoofing: A Survey
*   **Year:** 2023
*   **Authors:** Yu et al. (IEEE TPAMI)
*   **Key Finding:** A comprehensive review showing that texture analysis (MiniFASNet) is the modern standard for detecting 4K screen attacks.
*   **Status:** **Studied**. Referenced in "Future Scope" as the designated upgrade path for our Liveness module.
*   **Source:** [https://arxiv.org/abs/2106.14918](https://arxiv.org/abs/2106.14918)
