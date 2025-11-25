import torch
import numpy as np
from face_recognition import FaceRecognizer
from database import get_session, Encoding

def debug():
    print("--- Debugging Encoding Shape ---")
    
    # 1. Check Model Output
    try:
        fr = FaceRecognizer()
        dummy_face = np.random.randint(0, 255, (160, 160, 3), dtype=np.uint8)
        embedding = fr.get_embedding(dummy_face)
        print(f"Model Output Shape: {embedding.shape}")
        print(f"Model Output Dtype: {embedding.dtype}")
        print(f"Model Output Bytes: {len(embedding.tobytes())}")
    except Exception as e:
        print(f"Error checking model: {e}")

    # 2. Check Database Content
    print("\n--- Checking Database ---")
    session = get_session()
    try:
        encodings = session.query(Encoding).all()
        print(f"Found {len(encodings)} encodings.")
        for i, enc in enumerate(encodings):
            blob = enc.encoding_vector
            print(f"Encoding {i} ID {enc.id}: Blob Length = {len(blob)} bytes")
            
            # Try float32
            arr_f32 = np.frombuffer(blob, dtype=np.float32)
            print(f"  As float32: Shape {arr_f32.shape}")
            
            # Try float64
            arr_f64 = np.frombuffer(blob, dtype=np.float64)
            print(f"  As float64: Shape {arr_f64.shape}")
            
    except Exception as e:
        print(f"Error checking DB: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    debug()
