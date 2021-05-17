import sim          # librería para conectar con CoppeliaSim
import numpy as np
import sympy as sp
import cv2                      # opencv
import math
from skimage.measure import regionprops_table
import os

import torch, torchvision
torch.cuda.empty_cache()
import detectron2
from detectron2.utils.logger import setup_logger
setup_logger()
# import some common detectron2 utilities
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog, DatasetCatalog
from detectron2.data.datasets import register_coco_instances

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
    #cv2.imwrite("test.png", cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    return img

def get_objects(image):
    """
    Determina los objetos que hay en escena
    :param image: Imagen RGB extraida de la escena
    :return: Número de objetos presentes y imagen con los objetos etiquetados
    """
    img_GRAY = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    ret, im_bin = cv2.threshold(img_GRAY, 240, 255, cv2.THRESH_BINARY)
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
    props = regionprops_table(im_labels, properties=('centroid', 'orientation','major_axis_length','minor_axis_length'))
    centroid_x = props['centroid-0'][object_label - 1]
    centroid_y = props['centroid-1'][object_label - 1]
    orientation = props['orientation'][object_label - 1]
    #major_axis = props['major_axis_length'][object_label - 1]
    #minor_axis = props['minor_axis_length'][object_label - 1]
    return centroid_x, centroid_y, orientation

def build_predictor():
    cfg = get_cfg()
    # add project-specific config (e.g., TensorMask) here if you're not running a model in detectron2's core library
    cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5  # set threshold for this model
    # Find a model from detectron2's model zoo. You can use the https://dl.fbaipublicfiles... url as well
    cfg.MODEL.WEIGHTS = os.path.join(cfg.OUTPUT_DIR, "model_final.pth")
    cfg.MODEL.ROI_HEADS.NUM_CLASSES = 5
    predictor = DefaultPredictor(cfg)
    return predictor

def predict_image(image, predictor):
    outputs = predictor(image)
    return outputs

def get_object_n(outputs, n):
    objects_detected = outputs["instances"].pred_classes.cpu().numpy()
    i = np.where(n == objects_detected)[0][0]
    box = outputs["instances"].pred_boxes.tensor.cpu().numpy()[i]
    x = (box[2] - box[0]) / 2
    y = (box[3] - box[1]) / 2
    c_x = box[0] + x
    c_y = box[1] + y
    return int(c_y), int(c_x)

def get_objects_list(outputs, dict_objects2):
    objects_detected = outputs["instances"].pred_classes.cpu().numpy()
    objects_list = [dict_objects2[n] for n in objects_detected]
    return objects_list