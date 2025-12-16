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
    print("=== Face Attendi v2 Enrollment (RetinaFace + ArcFace) ===")
    name = input("Enter Name: ")
    email = input("Enter Email: ")
    
    # Initialize modules
    print("Initializing SOTA AI Models...")
    detector = FaceDetector()
    try:
        aligner = FaceAligner()
    except:
        aligner = None
        
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
            
        # Detect (RetinaFace)
        faces = detector.detect_faces(frame)
        
        # Viz
        frame_display = frame.copy()
        detector.draw_faces(frame_display, faces)
        
        cv2.putText(frame_display, f"Captured: {captured_count}/{required_samples}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        
        cv2.imshow("Enrollment", frame_display)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('c'):
            if len(faces) != 1:
                print("Please ensure exactly one face is visible.")
                continue
                
            face = faces[0]
            
            # Embedding (ArcFace 512D)
            embedding = face.embedding
            if embedding is None:
                print("Error: No embedding generated. Face might be too blurry/small.")
                continue
            
            # Save Image (Use Dlib Aligner for consistency, or Crop Box if unavailable)
            box = face.bbox.astype(int)
            save_image = None
            
            if aligner:
                try:
                     dlib_box = [box[0], box[1], box[2]-box[0], box[3]-box[1]]
                     landmarks = aligner.get_landmarks(frame, dlib_box)
                     save_image = aligner.align_face(frame, landmarks)
                except:
                     pass
            
            if save_image is None:
                # Fallback crop
                x1, y1, x2, y2 = max(0, box[0]), max(0, box[1]), min(frame.shape[1], box[2]), min(frame.shape[0], box[3])
                save_image = frame[y1:y2, x1:x2]
            
            # Save Logic
            timestamp = int(time.time())
            img_filename = f"{person_id}_{timestamp}.jpg"
            img_path = os.path.join(user_dir, img_filename)
            
            try:
                cv2.imwrite(img_path, save_image)
                add_encoding(person_id, embedding, img_path)
                captured_count += 1
                print(f"Captured sample {captured_count}/{required_samples}")
                time.sleep(0.5)
            except Exception as e:
                print(f"Error saving: {e}")
            
    cap.release()
    cv2.destroyAllWindows()
    
    if captured_count == required_samples:
        print(f"\nSuccessfully enrolled {name}!")
    else:
        print("\nEnrollment incomplete.")

if __name__ == "__main__":
    enroll_user()
