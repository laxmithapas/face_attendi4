# Face Recognition Attendance System

A robust, age-invariant, and fraud-resistant face recognition attendance system built with Python, FaceNet, and dlib.

## Features

- **Age-Invariant Recognition**: Uses FaceNet embeddings with adaptive thresholds for recent vs. old photos.
- **Appearance Variation Handling**: Captures multiple angles/expressions during enrollment.
- **Liveness Detection**: Prevents spoofing using Eye Aspect Ratio (blink detection).
- **Real-time Attendance**: Marks attendance automatically with confidence scores.
- **Enterprise-Grade Security**:
    - **Encryption**: Fernet (AES-128) encryption for biometric data.
    - **Access Control**: Password-protected dashboard with Session Timeout.
    - **Audit Trails**: Logs all login attempts and security events.
- **Admin Dashboard**: Streamlit-based interface to view logs and manage users.
- **Data Persistence**: SQLite database with SQLAlchemy ORM.

## 🛡️ Security & Privacy

This system is designed with "Privacy by Design" principles:

1.  **Biometric Encryption**: Face encodings are encrypted before storage. Even if the database is compromised, the data is unusable.
2.  **Session Security**: The Admin Dashboard enforces a **5-minute session timeout** to prevent unauthorized access.
3.  **Audit Logging**: A dedicated `audit_logs` table records every login success/failure and critical system action.
4.  **Secure Deletion**: Deleting a user triggers a "Cascading Delete" that wipes their profile, attendance history, and physical image files.

## 🔬 Research & Citations

This system is built upon industry-standard research in Deep Learning and Biometrics.

1.  **Deep Face Recognition**: Uses **FaceNet** (Inception ResNet V1) which maps faces into a Euclidean space where distances correspond to similarity.
    *   *Citation*: Deng, J., et al. "ArcFace: Additive Angular Margin Loss for Deep Face Recognition." (CVPR 2019).
2.  **Robust Face Detection**: Uses **MTCNN** (Multi-task Cascaded Convolutional Networks) for aligning faces before recognition.
    *   *Citation*: Zhang, K., et al. "Joint Face Detection and Alignment Using Multitask Cascaded Convolutional Networks." (IEEE Signal Processing Letters, 2016).
3.  **Anti-Spoofing (Liveness)**: Implements **Challenge-Response Protocols** (Randomized Head Turns/Smiles) to prevent Replay Attacks.
    *   *Citation*: "Face Anti-Spoofing Using Texture and Challenge-Response Protocols." (ResearchGate).

## Prerequisites

- Python 3.8+
- Webcam
- Visual Studio Build Tools (for dlib on Windows)

## Installation

1.  **Clone the repository**
    ```bash
    git clone <repository-url>
    cd face_attendi4
    ```

2.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```
    *Note: If `dlib` installation fails, ensure you have CMake and C++ build tools installed.*

3.  **Download Models**
    - The system uses `facenet-pytorch` which downloads models automatically.
    - You need `shape_predictor_68_face_landmarks.dat` for dlib.
    - Download it from [http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2](http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2), extract it, and place it in the `models/` directory.

## Usage

Run the main application:

```bash
python main.py
```

You will see a menu:
1.  **Enroll New User**: Capture face samples.
2.  **Start Attendance System**: Launch real-time recognition.
3.  **Launch Admin Dashboard**: Open the web interface.

### Enrollment
- Follow on-screen instructions.
- Capture 5 samples: Frontal, Left, Right, Smile, Neutral.

### Attendance
- The system will detect faces and check for liveness (blinking).
- Attendance is marked after consecutive frames of successful recognition + liveness check.
- `BLINK_THRESHOLD`: Liveness sensitivity.
- `CAMERA_ID`: Webcam index.

## Project Structure

- `main.py`: Entry point.
- `face_detection.py`: MTCNN wrapper.
- `face_recognition.py`: FaceNet embedding logic.
- `landmark_detection.py`: Dlib alignment.
- `liveness_detection.py`: Blink detection.
- `database.py`: Database models.
- `enrollment.py`: User registration script.
- `attendance.py`: Real-time loop.
- `dashboard.py`: Streamlit app.
