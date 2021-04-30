import sim          # librería para conectar con CoppeliaSim
import numpy as np
import sympy as sp
import cv2                      # opencv
import math
from skimage.measure import regionprops_table

def get_image(clientID, sensorHandle):
    """
    Recupera la imagen de la escena
    :param clientID: Coppelia ID
    :param sensorHandle: ID del handler del sensor de visión
    :return: La imagen de la escena
    """
    retCode, resolution, image = sim.simxGetVisionSensorImage(clientID, sensorHandle, 0, sim.simx_opmode_oneshot_wait)
    img = np.array(image, dtype=np.uint8)
    img.resize([resolution[1], resolution[0], 3])
    return img

def get_objects(image):
    """
    Determina los objetos que hay en escena
    :param image: Imagen RGB extraida de la escena
    :return: Número de objetos presentes y imagen con los objetos etiquetados
    """
    img_GRAY = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    ret, im_bin = cv2.threshold(img_GRAY, 150, 255, cv2.THRESH_BINARY)
    inv_im = cv2.bitwise_not(im_bin)
    n_labels, im_labels = cv2.connectedComponents(inv_im)
    return n_labels, im_labels

def get_centroids_orientation(object_label, im_labels):
    """
    Calcula el centroide del objeto seleccionado, además de su orientación
    :param object_label: Etiqueta del objeto seleccionado
    :param im_labels: Imagen con los objetos etiquetados
    :return: Coordenadas y orientación del centroide
    """
    props = regionprops_table(im_labels, properties=('centroid', 'orientation'))
    centroid_x = props['centroid-0'][object_label - 1]
    centroid_y = props['centroid-1'][object_label - 1]
    orientation = props['orientation'][object_label - 1]
    return centroid_x, centroid_y, orientation

