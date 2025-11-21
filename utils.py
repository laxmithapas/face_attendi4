import logging
import cv2
import numpy as np
from datetime import datetime

# Setup Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("system.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("FaceAuthSystem")

def get_logger():
    return logger

def resize_image(image, width=None, height=None):
    """Resize image while maintaining aspect ratio."""
    if width is None and height is None:
        return image
    
    (h, w) = image.shape[:2]
    
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))
        
    return cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

def rect_to_bb(rect):
    """Convert dlib rect to (x, y, w, h)."""
    x = rect.left()
    y = rect.top()
    w = rect.right() - x
    h = rect.bottom() - y
    return (x, y, w, h)

def shape_to_np(shape, dtype="int"):
    """Convert dlib shape object to numpy array of (x, y) coordinates."""
    coords = np.zeros((68, 2), dtype=dtype)
    for i in range(0, 68):
        coords[i] = (shape.part(i).x, shape.part(i).y)
    return coords
