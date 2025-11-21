import dlib
import cv2
import numpy as np
import os
from utils import shape_to_np, rect_to_bb
from config import MODELS_DIR

class FaceAligner:
    def __init__(self, predictor_path=None):
        if predictor_path is None:
            # Default to looking in models dir
            predictor_path = os.path.join(MODELS_DIR, "shape_predictor_68_face_landmarks.dat")
            
        if not os.path.exists(predictor_path):
            raise FileNotFoundError(f"Landmark predictor not found at {predictor_path}. Please download it.")
            
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(predictor_path)

    def get_landmarks(self, image, face_box):
        """
        Get 68 facial landmarks.
        Args:
            image: BGR numpy array
            face_box: (x, y, w, h) tuple or dlib.rectangle
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        if isinstance(face_box, (list, tuple, np.ndarray)):
            x, y, w, h = [int(v) for v in face_box]
            rect = dlib.rectangle(x, y, x + w, y + h)
        else:
            rect = face_box
            
        shape = self.predictor(gray, rect)
        return shape_to_np(shape)

    def align_face(self, image, landmarks, desiredLeftEye=(0.35, 0.35), desiredFaceWidth=160, desiredFaceHeight=160):
        """
        Align face based on eye centers.
        """
        # Extract the left and right eye (x, y)-coordinates
        (lStart, lEnd) = (42, 48)
        (rStart, rEnd) = (36, 42)
        
        leftEyePts = landmarks[lStart:lEnd]
        rightEyePts = landmarks[rStart:rEnd]
        
        # Compute the center of mass for each eye
        leftEyeCenter = leftEyePts.mean(axis=0).astype("int")
        rightEyeCenter = rightEyePts.mean(axis=0).astype("int")
        
        # Compute the angle between the eye centroids
        dY = rightEyeCenter[1] - leftEyeCenter[1]
        dX = rightEyeCenter[0] - leftEyeCenter[0]
        angle = np.degrees(np.arctan2(dY, dX)) - 180
        
        # Compute the desired right eye x-coordinate based on the
        # desired x-coordinate of the left eye
        desiredRightEyeX = 1.0 - desiredLeftEye[0]
        
        # Determine the scale of the new resulting image by taking
        # the ratio of the distance between eyes in the *current*
        # image to the ratio of distance between eyes in the
        # *desired* image
        dist = np.sqrt((dX ** 2) + (dY ** 2))
        desiredDist = (desiredRightEyeX - desiredLeftEye[0])
        desiredDist *= desiredFaceWidth
        scale = desiredDist / dist
        
        # Compute center (x, y)-coordinates (i.e., the median point)
        # between the two eyes in the input image
        eyesCenter = (int((leftEyeCenter[0] + rightEyeCenter[0]) // 2),
                      int((leftEyeCenter[1] + rightEyeCenter[1]) // 2))
        
        # Grab the rotation matrix for rotating and scaling the face
        M = cv2.getRotationMatrix2D(eyesCenter, angle, scale)
        
        # Update the translation component of the matrix
        tX = desiredFaceWidth * 0.5
        tY = desiredFaceHeight * desiredLeftEye[1]
        M[0, 2] += (tX - eyesCenter[0])
        M[1, 2] += (tY - eyesCenter[1])
        
        # Apply the affine transformation
        (w, h) = (desiredFaceWidth, desiredFaceHeight)
        output = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC)
        
        return output
