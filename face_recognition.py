from facenet_pytorch import InceptionResnetV1
import torch
import numpy as np
from scipy.spatial.distance import cosine
from config import THRESHOLD_RECENT, THRESHOLD_OLD, OLD_ENCODING_AGE_MONTHS
from datetime import datetime, timedelta

class FaceRecognizer:
    def __init__(self, device=None):
        self.device = device if device else torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        self.resnet = InceptionResnetV1(pretrained='vggface2').eval().to(self.device)
        print(f"FaceRecognizer initialized on {self.device}")

    def get_embedding(self, aligned_face):
        """
        Generate 512D embedding for an aligned face.
        Args:
            aligned_face: numpy array (160, 160, 3)
        Returns:
            embedding: numpy array (512,)
        """
        # Preprocess: Normalize and convert to tensor
        face_tensor = torch.from_numpy(aligned_face).permute(2, 0, 1).float().to(self.device)
        face_tensor = (face_tensor - 127.5) / 128.0  # Normalize to [-1, 1]
        face_tensor = face_tensor.unsqueeze(0)  # Add batch dimension

        with torch.no_grad():
            embedding = self.resnet(face_tensor).detach().cpu().numpy()
            
        return embedding.flatten()

    def match_face(self, target_embedding, known_encodings):
        """
        Match a face against a list of known encodings.
        Args:
            target_embedding: numpy array (512,)
            known_encodings: list of dicts {'person_id', 'encoding', 'created_at'}
        Returns:
            best_match_id: int or None
            confidence: float (0.0 to 1.0)
        """
        if not known_encodings:
            return None, 0.0

        best_score = 0.0
        best_match_id = None
        
        # Group encodings by person_id
        person_scores = {}

        for entry in known_encodings:
            person_id = entry['person_id']
            known_vec = entry['encoding']
            created_at = entry['created_at']

            # Calculate cosine similarity
            # Distance is 0 (same) to 2 (opposite). Similarity = 1 - (distance / 2)
            dist = cosine(target_embedding, known_vec)
            similarity = 1.0 - (dist / 2.0) # Normalize to 0-1 roughly, though cosine dist is usually 0-2. 
            # Better: Cosine Similarity is dot(A,B)/(norm(A)*norm(B)). 
            # scipy cosine returns 1 - similarity. So similarity = 1 - dist.
            similarity = 1.0 - dist

            # Determine threshold based on age of encoding
            age_months = (datetime.now() - created_at).days / 30.0
            threshold = THRESHOLD_OLD if age_months > OLD_ENCODING_AGE_MONTHS else THRESHOLD_RECENT
            
            # Weighting logic: Recent encodings have higher weight
            weight = 1.0 if age_months <= OLD_ENCODING_AGE_MONTHS else 0.8
            
            if similarity > threshold:
                if person_id not in person_scores:
                    person_scores[person_id] = []
                person_scores[person_id].append((similarity, weight))

        # Aggregate scores for each person
        final_results = []
        for pid, scores in person_scores.items():
            # Weighted average of top 3 matches
            scores.sort(key=lambda x: x[0], reverse=True)
            top_scores = scores[:3]
            
            total_weight = sum(w for s, w in top_scores)
            weighted_sum = sum(s * w for s, w in top_scores)
            
            avg_score = weighted_sum / total_weight if total_weight > 0 else 0
            final_results.append((pid, avg_score))

        if not final_results:
            return None, 0.0

        # Get best match
        final_results.sort(key=lambda x: x[1], reverse=True)
        best_match_id, best_score = final_results[0]

        return best_match_id, best_score
