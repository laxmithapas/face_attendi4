import os

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'attendance.db')
MODELS_DIR = os.path.join(BASE_DIR, 'models')
ENROLLMENT_DIR = os.path.join(BASE_DIR, 'enrollment_images')

# Create directories if they don't exist
os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(ENROLLMENT_DIR, exist_ok=True)

# Database
DATABASE_URI = f'sqlite:///{DB_PATH}'

# Face Recognition Thresholds (ArcFace - Cosine Similarity)
# Range: -1.0 to 1.0. Higher is better match.
# 0.35 is a balanced threshold for ArcFace (buffalo_l)
THRESHOLD_RECENT = 0.35
THRESHOLD_OLD = 0.30
OLD_ENCODING_AGE_MONTHS = 3
RE_ENROLLMENT_PERIOD_MONTHS = 6

# InsightFace Settings
INSIGHTFACE_MODEL = 'buffalo_l'
CTX_ID = 0 # 0 for GPU, -1 for CPU. Using -1 for safety unless CUDA found. (Detector handles this)

# Camera
CAMERA_ID = 0
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

# Liveness
BLINK_THRESHOLD = 0.25  # Eye Aspect Ratio
CONSECUTIVE_FRAMES = 3

# Performance
PROCESS_EVERY_N_FRAMES = 3
