import cv2
import os
import time
import numpy as np
from face_detection import FaceDetector
from landmark_detection import FaceAligner
from face_recognition import FaceRecognizer
from database import add_person, add_encoding
from config import ENROLLMENT_DIR, CAMERA_ID, FRAME_WIDTH, FRAME_HEIGHT
from utils import get_logger

logger = get_logger()

def enroll_user():
    print("=== Face Recognition Enrollment ===")
    name = input("Enter Name: ")
    email = input("Enter Email: ")
    
    # Initialize modules
    print("Initializing system...")
    detector = FaceDetector()
    aligner = FaceAligner()
    recognizer = FaceRecognizer()
    
    # Create person in DB
    person_id = add_person(name, email)
    if not person_id:
        print("Error creating user in database.")
        return

    # Create user directory
    user_dir = os.path.join(ENROLLMENT_DIR, str(person_id))
    os.makedirs(user_dir, exist_ok=True)
    
    cap = cv2.VideoCapture(CAMERA_ID)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
    
    captured_count = 0
    required_samples = 5
    
    print(f"\nStarting capture. Please look at the camera.")
    print("We need 5 samples. Press 'c' to capture, 'q' to quit.")
    print("Instructions: 1. Frontal, 2. Slight Left, 3. Slight Right, 4. Smile, 5. Neutral")
    
    while captured_count < required_samples:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break
            
        # Detect face for visualization
        boxes, probs, _ = detector.detect_faces(frame)
        frame_display = frame.copy()
        detector.draw_faces(frame_display, boxes, probs)
        
        cv2.putText(frame_display, f"Captured: {captured_count}/{required_samples}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        
        cv2.imshow("Enrollment", frame_display)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('c'):
            if len(boxes) != 1:
                print("Please ensure exactly one face is visible.")
                continue
                
            # Process the frame
            # 1. Detect landmarks
            box = boxes[0]
            landmarks = aligner.get_landmarks(frame, box)
            
            # 2. Align face
            aligned_face = aligner.align_face(frame, landmarks)
            
            # 3. Generate embedding
            embedding = recognizer.get_embedding(aligned_face)
            
            # 4. Save image and embedding
            timestamp = int(time.time())
            img_filename = f"{person_id}_{timestamp}.jpg"
            img_path = os.path.join(user_dir, img_filename)
            cv2.imwrite(img_path, aligned_face)
            
            add_encoding(person_id, embedding, img_path)
            
            captured_count += 1
            print(f"Captured sample {captured_count}/{required_samples}")
            time.sleep(0.5) # Prevent accidental double capture
            
    cap.release()
    cv2.destroyAllWindows()
    
    if captured_count == required_samples:
        print(f"\nSuccessfully enrolled {name} with {captured_count} samples.")
    else:
        print("\nEnrollment incomplete.")

if __name__ == "__main__":
    enroll_user()
