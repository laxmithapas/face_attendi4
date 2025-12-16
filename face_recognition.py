import numpy as np
from datetime import datetime
from config import THRESHOLD_RECENT, THRESHOLD_OLD, OLD_ENCODING_AGE_MONTHS
import io
# InsightFace embeddings are numpy arrays directly

class FaceRecognizer:
    def __init__(self, device=None):
        print("FaceRecognizer (ArcFace) initialized. (Using embeddings from Detector)")

    def get_embedding(self, face_object):
        """
        Extract embedding from the InsightFace object.
        Args:
            face_object: The object returned by detector.detect_faces()
        Returns:
            embedding: numpy array (512,)
        """
        return face_object.embedding

    def match_face(self, target_embedding, known_encodings):
        """
        Match a face against a list of known encodings using Cosine Similarity.
        Args:
            target_embedding: numpy array (512,)
            known_encodings: list of dicts
        Returns:
            best_match_id: int or None
            confidence: float (0.0 to 1.0)
        """
        if not known_encodings:
            return None, 0.0

        best_score = 0.0
        best_match_id = None
        
        # Prepare target for matrix multiplication (normalize just in case)
        target_norm = np.linalg.norm(target_embedding)
        if target_norm == 0: return None, 0.0
        target_embedding = target_embedding / target_norm

        person_scores = {}

        for entry in known_encodings:
            person_id = entry['person_id']
            
            try:
                # Load stored embedding
                if isinstance(entry['encoding'], bytes):
                   try:
                       known_vec = np.load(io.BytesIO(entry['encoding']))
                   except:
                       known_vec = np.frombuffer(entry['encoding'], dtype=np.float32)
                else:
                   known_vec = entry['encoding']

                # Normalize known vector
                known_norm = np.linalg.norm(known_vec)
                if known_norm == 0: continue
                known_vec = known_vec / known_norm

                # Cosine Similarity = Dot product of normalized vectors
                similarity = np.dot(target_embedding, known_vec)
                
                # ArcFace Threshold is typically around 0.25 - 0.4 depending on strictness
                # We use config thresholds but might need to tune them for ArcFace
                # Let's assume standard thresholds for now (0.4 is strict, 0.3 is loose)
                
                created_at = entry['created_at']
                age_months = (datetime.now() - created_at).days / 30.0
                weight = 1.0 if age_months <= OLD_ENCODING_AGE_MONTHS else 0.8

                if similarity > 0.35: # Hardcoded ArcFace base threshold
                     if person_id not in person_scores:
                        person_scores[person_id] = []
                     person_scores[person_id].append((similarity, weight))

            except Exception as e:
                continue

        # Aggregate scores
        final_results = []
        for pid, scores in person_scores.items():
            scores.sort(key=lambda x: x[0], reverse=True)
            top_scores = scores[:3]
            processed_score = sum(s * w for s, w in top_scores) / sum(w for s, w in top_scores)
            final_results.append((pid, processed_score))

        if not final_results:
            return None, 0.0

        final_results.sort(key=lambda x: x[1], reverse=True)
        best_match_id, best_score = final_results[0]
        
        return best_match_id, best_score
