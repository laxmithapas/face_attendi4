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

# Face Recognition Thresholds
THRESHOLD_RECENT = 0.6
THRESHOLD_OLD = 0.55
OLD_ENCODING_AGE_MONTHS = 3
RE_ENROLLMENT_PERIOD_MONTHS = 6

# Camera
CAMERA_ID = 0
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

# Liveness
BLINK_THRESHOLD = 0.25  # Eye Aspect Ratio
CONSECUTIVE_FRAMES = 3

# Performance
PROCESS_EVERY_N_FRAMES = 3
