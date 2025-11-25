import pickle
import numpy as np
from database import get_session, Encoding

def debug():
    print("--- Debugging Pickle ---")
    session = get_session()
    try:
        encodings = session.query(Encoding).all()
        if not encodings:
            print("No encodings found.")
            return

        blob = encodings[0].encoding_vector
        print(f"Blob length: {len(blob)}")
        
        try:
            data = pickle.loads(blob)
            print("Success! Unpickled data.")
            print(f"Type: {type(data)}")
            if isinstance(data, np.ndarray):
                print(f"Shape: {data.shape}")
                print(f"Dtype: {data.dtype}")
        except Exception as e:
            print(f"Failed to unpickle: {e}")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    debug()
