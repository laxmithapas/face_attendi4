import cv2
import numpy as np
from insightface.app import FaceAnalysis
from config import FRAME_WIDTH, FRAME_HEIGHT

class FaceDetector:
    def __init__(self, device=None):
        # Initialize InsightFace with RetinaFace + ArcFace
        # allowed_modules=['detection', 'recognition'] is default
        self.app = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'])
        self.app.prepare(ctx_id=0, det_size=(640, 640))
        print(f"FaceDetector (InsightFace) initialized.")

    def detect_faces(self, frame):
        """
        Detect faces in a frame using RetinaFace.
        Args:
            frame: numpy array (BGR)
        Returns:
            faces: list of InsightFace Face objects (contains bbox, kps, embedding)
        """
        # InsightFace expects BGR (OpenCV format) directly
        faces = self.app.get(frame)
        
        return faces

    def draw_faces(self, frame, faces):
        """Draw bounding boxes and landmarks."""
        for face in faces:
            # Bounding Box
            box = face.bbox.astype(int)
            cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2)
            
            # Landmarks (5 points)
            if face.kps is not None:
                for kp in face.kps:
                    cv2.circle(frame, (int(kp[0]), int(kp[1])), 2, (0, 0, 255), -1)
                    
            # Score
            if face.det_score:
                 cv2.putText(frame, f"{face.det_score:.2f}", (box[0], box[1] - 10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                           
        return frame
