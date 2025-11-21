from facenet_pytorch import MTCNN
import torch
import numpy as np
from PIL import Image
import cv2
from config import FRAME_WIDTH, FRAME_HEIGHT

class FaceDetector:
    def __init__(self, device=None):
        self.device = device if device else torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        self.mtcnn = MTCNN(
            keep_all=True,
            device=self.device,
            min_face_size=40,
            thresholds=[0.6, 0.7, 0.7]
        )
        print(f"FaceDetector initialized on {self.device}")

    def detect_faces(self, frame):
        """
        Detect faces in a frame.
        Args:
            frame: numpy array (BGR) from cv2
        Returns:
            boxes: list of bounding boxes [x1, y1, x2, y2]
            probs: list of probabilities
            landmarks: list of 5 facial landmarks (eyes, nose, mouth)
        """
        # Convert BGR to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        
        # Detect faces
        boxes, probs, landmarks = self.mtcnn.detect(img, landmarks=True)
        
        if boxes is None:
            return [], [], []
            
        return boxes, probs, landmarks

    def draw_faces(self, frame, boxes, probs=None):
        """Draw bounding boxes on the frame."""
        for i, box in enumerate(boxes):
            x1, y1, x2, y2 = [int(b) for b in box]
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            if probs is not None:
                cv2.putText(frame, f"{probs[i]:.2f}", (x1, y1 - 10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        return frame
