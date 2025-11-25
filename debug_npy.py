import numpy as np
import io
from database import get_session, Encoding

def debug():
    print("--- Debugging NPY Format ---")
    session = get_session()
    try:
        encodings = session.query(Encoding).all()
        if not encodings:
            print("No encodings found.")
            return

        blob = encodings[0].encoding_vector
        print(f"Blob length: {len(blob)}")
        
        try:
            # Try loading as .npy
            bio = io.BytesIO(blob)
            data = np.load(bio)
            print("Success! Loaded as .npy")
            print(f"Shape: {data.shape}")
            print(f"Dtype: {data.dtype}")
        except Exception as e:
            print(f"Failed to load as .npy: {e}")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    debug()
