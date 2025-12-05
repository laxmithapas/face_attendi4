import cv2
import time
import numpy as np
from face_detection import FaceDetector
from landmark_detection import FaceAligner
from face_recognition import FaceRecognizer
from liveness_detection import LivenessDetector
from database import get_all_encodings, mark_attendance, get_monthly_attendance_count, get_session, Person
from config import CAMERA_ID, FRAME_WIDTH, FRAME_HEIGHT, PROCESS_EVERY_N_FRAMES, CONSECUTIVE_FRAMES
from utils import get_logger

logger = get_logger()

def run_attendance_system():
    print("=== Face Recognition Attendance System ===")
    print("Loading models and data...")
    
    detector = FaceDetector()
    aligner = FaceAligner()
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
    
    import random
    
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
    
    # State tracking per person
    # {person_id: {'state': CHALLENGE_X, 'start_time': t, 'passed': bool}}
    user_states = {}
    
    frame_count = 0
    recognition_cache = [] # List of dicts for current frame faces
    print("Starting video stream. Press 'q' to quit.")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        frame_count += 1
        current_time = time.time()
        
        # Detect faces
        boxes, probs, landmarks_list = detector.detect_faces(frame)
        
        # Reset cache if new detection cycle (optional, but we want to keep it for N frames)
        # Actually, if the number of faces changes, our index-based cache breaks.
        # Simple fix: If frame_count % N == 0, we clear cache inside the loop logic?
        # No, we clear it here if it's a recognition frame.
        if frame_count % PROCESS_EVERY_N_FRAMES == 0:
            recognition_cache = []
        
        # Draw boxes
        detector.draw_faces(frame, boxes, probs)
        
        for i, box in enumerate(boxes):
            # Get dlib landmarks for advanced liveness
            dlib_landmarks = aligner.get_landmarks(frame, box)
            
            # Check liveness metrics
            liveness_data = liveness.check_liveness(dlib_landmarks, FRAME_WIDTH, FRAME_HEIGHT)
            
            # Recognition (Identify who it is first)
            name = "Unknown"
            confidence = 0.0
            person_id = None
            
            # Caching logic to prevent flickering
            # We use a simple index-based matching since N is small (3 frames)
            # In a complex app, we would use centroid tracking
            
            if frame_count % PROCESS_EVERY_N_FRAMES == 0:
                aligned_face = aligner.align_face(frame, dlib_landmarks)
                embedding = recognizer.get_embedding(aligned_face)
                person_id, confidence = recognizer.match_face(embedding, known_data)
                
                # Update cache
                if len(recognition_cache) <= i:
                    recognition_cache.append({})
                recognition_cache[i] = {'person_id': person_id, 'confidence': confidence}
            else:
                # Use cached result if available
                if i < len(recognition_cache):
                    cached = recognition_cache[i]
                    person_id = cached.get('person_id')
                    confidence = cached.get('confidence', 0.0)
            
            if person_id:
                name = person_names.get(person_id, "Unknown")
                
                # Initialize state if new
                if person_id not in user_states:
                    user_states[person_id] = {
                        'challenge': CHALLENGE_NONE,
                        'last_challenge_time': 0,
                        'verified': False
                    }
                
                state = user_states[person_id]
                
                # Cooldown check for attendance
                last_marked = getattr(run_attendance_system, 'last_marked', {})
                is_marked_recently = person_id in last_marked and (current_time - last_marked[person_id] < 60)
                
                if is_marked_recently:
                     cv2.putText(frame, "Attendance Marked!", (int(box[0]), int(box[1]) - 50),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                     state['challenge'] = CHALLENGE_NONE # Reset
                
                elif not state['verified']:
                    # Logic: Issue a challenge if none active
                    if state['challenge'] == CHALLENGE_NONE:
                        # Pick a random challenge
                        state['challenge'] = random.choice([CHALLENGE_BLINK, CHALLENGE_SMILE, CHALLENGE_LEFT, CHALLENGE_RIGHT])
                        state['challenge_start'] = current_time
                    
                    # Check Challenge Compliance
                    challenge = state['challenge']
                    passed = False
                    
                    if challenge == CHALLENGE_BLINK:
                        if liveness_data['is_blinking']:
                            passed = True
                    elif challenge == CHALLENGE_SMILE:
                        if liveness_data['is_smiling']:
                            passed = True
                    elif challenge == CHALLENGE_LEFT:
                        if liveness_data['head_pose'] == "LEFT":
                            passed = True
                    elif challenge == CHALLENGE_RIGHT:
                        if liveness_data['head_pose'] == "RIGHT":
                            passed = True
                            
                    # Display Challenge
                    text = CHALLENGE_TEXTS[challenge]
                    cv2.putText(frame, text, (int(box[0]), int(box[1]) - 30),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 165, 255), 2)
                               
                    # If passed
                    if passed:
                        # Mark attendance!
                        success = mark_attendance(person_id, confidence)
                        if success:
                            state['verified'] = True
                            state['challenge'] = CHALLENGE_NONE
                            
                            # Update global cooldown
                            last_marked[person_id] = current_time
                            run_attendance_system.last_marked = last_marked
                            
                            cv2.putText(frame, "SUCCESS!", (int(box[0]), int(box[1]) - 60),
                                       cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 3)
                    
                    # Timeout (5 seconds) -> Reset to new challenge
                    if current_time - state['challenge_start'] > 5.0:
                        state['challenge'] = CHALLENGE_NONE
                
            # Display info (Name at BOTTOM)
            color = (0, 255, 0) if person_id else (0, 0, 255)
            label = f"{name} ({confidence:.2f})"
            
            # Draw background for name
            (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
            cv2.rectangle(frame, (int(box[0]), int(box[1] + box[3])), (int(box[0] + w), int(box[1] + box[3] + h + 10)), color, -1)
            
            cv2.putText(frame, label, (int(box[0]), int(box[1] + box[3] + 15)),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            # Debug info for pose
            # cv2.putText(frame, f"Y:{liveness_data['yaw']:.0f} P:{liveness_data['pitch']:.0f}", (10, 50 + 20*i), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)

        cv2.imshow("Attendance System", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_attendance_system()
