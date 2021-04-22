# importamos las librerías necesarias
import sim          # librería para conectar con CoppeliaSim
import numpy as np
import sympy as sp
import cv2                      # opencv
#import matplotlib.pyplot as plt # pyplot

def get_image(clientID, sensorHandle):
    retCode, resolution, image = sim.simxGetVisionSensorImage(clientID, sensorHandle, 0, sim.simx_opmode_oneshot_wait)
    img = np.array(image, dtype=np.uint8)
    img.resize([resolution[1], resolution[0], 3])

    return img

def process_image(img):
    #img_BGR = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    img_GRAY = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    ret, thresh = cv2.threshold(img_GRAY, 150, 255, cv2.THRESH_BINARY)
    detector = cv2.SimpleBlobDetector_create()  # Verion antigua !!
    keypoints = detector.detect(thresh)

    return keypoints