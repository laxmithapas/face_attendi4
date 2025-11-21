from scipy.spatial import distance as dist
from config import BLINK_THRESHOLD
import numpy as np
import cv2

class LivenessDetector:
    def __init__(self):
        # Eye landmarks indices (dlib 68 points)
        self.LEFT_EYE_IDXS = list(range(36, 42))
        self.RIGHT_EYE_IDXS = list(range(42, 48))
        # Mouth indices
        self.MOUTH_IDXS = list(range(48, 68))
        
        # 3D model points for generic face (in mm)
        self.model_points = np.array([
            (0.0, 0.0, 0.0),             # Nose tip
            (0.0, -330.0, -65.0),        # Chin
            (-225.0, 170.0, -135.0),     # Left eye left corner
            (225.0, 170.0, -135.0),      # Right eye right corner
            (-150.0, -150.0, -125.0),    # Left Mouth corner
            (150.0, -150.0, -125.0)      # Right mouth corner
        ])

    def eye_aspect_ratio(self, eye):
        """Compute the eye aspect ratio (EAR)."""
        A = dist.euclidean(eye[1], eye[5])
        B = dist.euclidean(eye[2], eye[4])
        C = dist.euclidean(eye[0], eye[3])
        ear = (A + B) / (2.0 * C)
        return ear
        
    def mouth_aspect_ratio(self, mouth):
        """Compute the mouth aspect ratio (MAR) for smile detection."""
        # Vertical distances
        A = dist.euclidean(mouth[2], mouth[10]) # 51, 59
        B = dist.euclidean(mouth[4], mouth[8])  # 53, 57
        # Horizontal distance
        C = dist.euclidean(mouth[0], mouth[6])  # 48, 54
        mar = (A + B) / (2.0 * C)
        return mar

    def get_head_pose(self, shape):
        """
        Calculates the face angle (yaw) to detect if user is looking Left, Right, or Center.
        Uses the distance between eyes and nose edge.
        """
        # Dlib landmark indices (numpy array)
        # shape is (68, 2)
        left_eye_outer = shape[36][0]
        right_eye_outer = shape[45][0]
        nose_tip = shape[30][0]

        # Calculate distances from nose to edges of eyes
        dist_left = np.abs(nose_tip - left_eye_outer)
        dist_right = np.abs(right_eye_outer - nose_tip)

        # Calculate ratio
        # If ratio is close to 1, face is Center.
        # If ratio > 1.5 or < 0.6, face is turned.
        if dist_right == 0: return "CENTER" # Avoid division by zero
        ratio = dist_left / dist_right

        if ratio < 0.6:
            return "RIGHT"
        elif ratio > 1.6:
            return "LEFT"
        else:
            return "CENTER"

    def detect_smile(self, shape):
        """Check if person is smiling based on MAR."""
        mouth = shape[self.MOUTH_IDXS]
        mar = self.mouth_aspect_ratio(mouth)
        # Simple MAR threshold for "Mouth Open / Big Smile"
        return mar > 0.3, mar

    def check_liveness(self, landmarks, frame_width, frame_height):
        """
        Comprehensive liveness check.
        Returns: dict of states
        """
        leftEye = landmarks[self.LEFT_EYE_IDXS]
        rightEye = landmarks[self.RIGHT_EYE_IDXS]
        
        # Blink
        leftEAR = self.eye_aspect_ratio(leftEye)
        rightEAR = self.eye_aspect_ratio(rightEye)
        avg_ear = (leftEAR + rightEAR) / 2.0
        is_blinking = avg_ear < BLINK_THRESHOLD
        
        # Head Pose (Simple Ratio)
        head_pose = self.get_head_pose(landmarks)
        
        # Smile
        is_smiling, mar = self.detect_smile(landmarks)
        
        return {
            "is_blinking": is_blinking,
            "ear": avg_ear,
            "head_pose": head_pose,
            "is_smiling": is_smiling,
            "mar": mar
        }
