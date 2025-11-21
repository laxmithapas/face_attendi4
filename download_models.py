import urllib.request
import bz2
import os
import shutil
from config import MODELS_DIR

def download_dlib_model():
    print("Checking for dlib model...")
    
    model_filename = "shape_predictor_68_face_landmarks.dat"
    model_path = os.path.join(MODELS_DIR, model_filename)
    
    if os.path.exists(model_path):
        print(f"✅ Model already exists at: {model_path}")
        return

    # Use GitHub mirror for faster download
    url = "https://github.com/davisking/dlib-models/raw/master/shape_predictor_68_face_landmarks.dat.bz2"
    bz2_filename = model_filename + ".bz2"
    bz2_path = os.path.join(MODELS_DIR, bz2_filename)

    try:
        print(f"⬇️  Downloading model from {url}...")
        print("This might take a minute (64MB)...")
        
        # Try using curl first (usually faster/reliable on Windows)
        import subprocess
        try:
            subprocess.run(["curl", "-L", "-o", bz2_path, url], check=True)
            print("✅ Download complete (via curl).")
        except (subprocess.SubprocessError, FileNotFoundError):
            print("⚠️ curl failed, falling back to Python download...")
            import ssl
            context = ssl._create_unverified_context()
            with urllib.request.urlopen(url, context=context) as response, open(bz2_path, 'wb') as out_file:
                shutil.copyfileobj(response, out_file)
            print("✅ Download complete (via Python).")
        
        print("📦 Extracting model...")
        with bz2.BZ2File(bz2_path) as fr, open(model_path, 'wb') as fw:
            shutil.copyfileobj(fr, fw)
            
        if os.path.exists(bz2_path):
            os.remove(bz2_path)
            
        print(f"✅ Extracted to: {model_path}")
        print("🎉 You are ready to go!")
        
    except Exception as e:
        print(f"❌ Error downloading model: {e}")
        print("Please download manually from: http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2")
        print(f"Save it to: {model_path}")

if __name__ == "__main__":
    download_dlib_model()
