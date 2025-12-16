import cv2
import time
import numpy as np
import random
from face_detection import FaceDetector
from landmark_detection import FaceAligner
from face_recognition import FaceRecognizer
from liveness_detection import LivenessDetector
from database import get_all_encodings, mark_attendance, get_session, Person
from config import CAMERA_ID, FRAME_WIDTH, FRAME_HEIGHT, PROCESS_EVERY_N_FRAMES
from utils import get_logger

logger = get_logger()

def run_attendance_system():
    print("=== Face Attendi v2 (SOTA Upgrade) ===")
    print("Initializing RetinaFace (Detection) & ArcFace (Recognition)...")
    
    # Initialize Modules
    detector = FaceDetector()
    try:
        # We need FaceAligner for DLIB landmarks (Liveness)
        aligner = FaceAligner()
    except Exception as e:
        print(f"Warning: Landmark predictor not found. Liveness will fail. {e}")
        aligner = None

    recognizer = FaceRecognizer()
    liveness = LivenessDetector()
    
    # Load known encodings
    known_data = get_all_encodings()
    print(f"Loaded {len(known_data)} encodings.")
    
    # Cache person names
    session = get_session()
    persons = session.query(Person).all()
    person_names = {p.id: p.name for p in persons}
    session.close()
    
    cap = cv2.VideoCapture(CAMERA_ID)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
    
    # Challenge states
    CHALLENGE_NONE = 0
    CHALLENGE_BLINK = 1
    CHALLENGE_SMILE = 2
    CHALLENGE_LEFT = 3
    CHALLENGE_RIGHT = 4
    
    CHALLENGE_TEXTS = {
        CHALLENGE_NONE: "Verifying...",
        CHALLENGE_BLINK: "PLEASE BLINK EYES",
        CHALLENGE_SMILE: "PLEASE SMILE",
        CHALLENGE_LEFT: "TURN HEAD LEFT",
        CHALLENGE_RIGHT: "TURN HEAD RIGHT"
    }
    
    # {person_id: {'state': CHALLENGE_X, 'start_time': t, 'passed': bool}}
    user_states = {}
    
    frame_count = 0
    recognition_cache = {} # Map i -> {pid, conf}
    
    print("Starting video stream. Press 'q' to quit.")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        frame_count += 1
        current_time = time.time()
        
        # 1. Detection (RetinaFace)
        # Returns list of InsightFace Face objects
        faces = detector.detect_faces(frame)
        
        # 2. Draw Basic Boxes
        detector.draw_faces(frame, faces)

        # Clear cache if scene changed drastically? 
        # For simplicity in v2, we re-verify every N frames but track by index `i` is risky if faces swap.
        # But InsightFace is fast enough (0.1s) we might run recognition EVERY frame on GPU?
        # On CPU it might struggle. Let's keep N=3 optimization.
        
        for i, face in enumerate(faces):
            box = face.bbox.astype(int) # x1, y1, x2, y2
            
            # 3. Liveness Check (EAR via Dlib)
            # We need 68 landmarks for EAR. InsightFace only gives 5.
            # Convert [x1, y1, x2, y2] to [x, y, w, h] for dlib
            dlib_box = [box[0], box[1], box[2]-box[0], box[3]-box[1]]
            
            liveness_data = {
                "is_blinking": False,
                "is_smiling": False,
                "head_pose": "CENTER"
            }
            
            if aligner:
                try:
                    dlib_landmarks = aligner.get_landmarks(frame, dlib_box)
                    liveness_data = liveness.check_liveness(dlib_landmarks, FRAME_WIDTH, FRAME_HEIGHT)
                except Exception:
                    pass # Face might be out of bounds for dlib

            # 4. Recognition (ArcFace)
            name = "Unknown"
            confidence = 0.0
            person_id = None
            
            # Use cached result if valid
            if frame_count % PROCESS_EVERY_N_FRAMES != 0 and i in recognition_cache:
                cached = recognition_cache[i]
                person_id = cached['person_id']
                confidence = cached['confidence']
            else:
                # Run Matching
                # InsightFace already computed the embedding!
                if face.embedding is not None:
                    person_id, confidence = recognizer.match_face(face.embedding, known_data)
                    recognition_cache[i] = {'person_id': person_id, 'confidence': confidence}
            
            # 5. Application Logic
            if person_id:
                name = person_names.get(person_id, "Unknown")
                
                # Initialize state
                if person_id not in user_states:
                    user_states[person_id] = {
                        'challenge': CHALLENGE_NONE,
                        'last_challenge_time': 0,
                        'verified': False
                    }
                
                state = user_states[person_id]
                
                # Cooldown check
                last_marked = getattr(run_attendance_system, 'last_marked', {})
                is_marked_recently = person_id in last_marked and (current_time - last_marked[person_id] < 60)
                
                if is_marked_recently:
                     cv2.putText(frame, "Attendance Marked!", (box[0], box[1] - 50),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                     state['challenge'] = CHALLENGE_NONE
                
                elif not state['verified']:
                    if state['challenge'] == CHALLENGE_NONE:
                        state['challenge'] = random.choice([CHALLENGE_BLINK, CHALLENGE_SMILE, CHALLENGE_LEFT, CHALLENGE_RIGHT])
                        state['challenge_start'] = current_time
                    
                    challenge = state['challenge']
                    passed = False
                    
                    if challenge == CHALLENGE_BLINK and liveness_data['is_blinking']: passed = True
                    if challenge == CHALLENGE_SMILE and liveness_data['is_smiling']: passed = True
                    if challenge == CHALLENGE_LEFT and liveness_data['head_pose'] == "LEFT": passed = True
                    if challenge == CHALLENGE_RIGHT and liveness_data['head_pose'] == "RIGHT": passed = True
                            
                    text = CHALLENGE_TEXTS[challenge]
                    cv2.putText(frame, text, (box[0], box[1] - 30),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 165, 255), 2)
                               
                    if passed:
                        success = mark_attendance(person_id, confidence)
                        if success:
                            state['verified'] = True
                            state['challenge'] = CHALLENGE_NONE
                            last_marked[person_id] = current_time
                            run_attendance_system.last_marked = last_marked
                            
                            cv2.putText(frame, "SUCCESS!", (box[0], box[1] - 60),
                                       cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 3)
                    
                    if current_time - state['challenge_start'] > 5.0:
                        state['challenge'] = CHALLENGE_NONE

            # UI Labels
            color = (0, 255, 0) if person_id else (0, 0, 255)
            label = f"{name}"
            # ArcFace confidence is -1 to 1. 0.4+ is good math.
            if person_id: label += f" ({confidence:.2f})"
            
            cv2.putText(frame, label, (box[0], box[3] + 20),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        cv2.imshow("Face Attendi v2 (RetinaFace+ArcFace)", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_attendance_system()
