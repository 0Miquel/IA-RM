from visualize_fun import *
from coppelia_fun import *
from movement_fun import *

import pygame

import torch, torchvision
torch.cuda.empty_cache()
import detectron2
from detectron2.utils.logger import setup_logger
setup_logger()

pygame.init()

screen = pygame.display.set_mode((512, 512))
pygame.display.set_caption('IA-RM')

predictor = build_predictor()
dict_objects2 = {0:"apple", 1:"banana", 2:"glass", 3:"orange", 4:"tv controller"}
dict_objects = {"apple":0, "banana":1, "glass":2, "orange":3, "tv controller":4}

clientID = connect(19999)
grip, joint1, joint2, joint3, joint4, joint5, dummy, sensorHandle, psensor = get_ids(clientID)
list_joints = [joint1, joint2, joint3, joint4]

object_grabbed = False
running = True

while running:
    image = get_image(clientID, sensorHandle)

    surface = pygame.surfarray.make_surface(image)
    screen.blit(surface, (0, 0))
    pygame.display.update()

    if not object_grabbed:
        word = input("Enter object: ")
        ######
        outputs = predict_image(image, predictor)
        objects_list = get_objects_list(outputs, dict_objects2)
        print(objects_list)
        y, x = get_object_n(outputs, dict_objects[word])
        ######
        n_objects, im_labels = get_objects(image)

        object_label = im_labels[y, x]
        y, x, orientation = get_centroids_orientation(object_label, im_labels)
        xf = np.around(0.5 - x * 0.5 / 512, 3)
        yf = np.around(0.5 - y * 0.5 / 512, 3)
        print(f"x = {xf}, y = {yf}, orientation = {orientation}")
        correction_degree, reachable = movement_sequence(xf, yf, 0.25, list_joints, clientID)

        if reachable:
            time.sleep(1)
            move_joint5(clientID, joint5, orientation, correction_degree)

            time.sleep(1)
            all_degrees = line(xf,yf,0.25)
            object_handler, zf = grab_object(all_degrees, clientID, list_joints, psensor)

            time.sleep(1)
            gripper(clientID, 1, object_handler)

            time.sleep(1)
            all_degrees = line_up(xf, yf, zf - 0.5, 0.25)
            move_line(all_degrees, clientID, list_joints)
            object_grabbed = True

    elif object_grabbed:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                y, x = pygame.mouse.get_pos()
                xf = np.around(0.5 - x * 0.5 / 512, 3)
                yf = np.around(0.5 - y * 0.5 / 512, 3)

                print(f"x = {xf}, y = {yf}")
                _, reachable = movement_sequence(xf, yf, 0.25, list_joints, clientID)

                if reachable:
                    time.sleep(1)
                    all_degrees = line_down(xf, yf, 0.25, zf-0.5)
                    move_line(all_degrees, clientID, list_joints)

                    time.sleep(1)
                    gripper(clientID, 0, object_handler)

                    time.sleep(1)
                    all_degrees = line_up(xf, yf, zf - 0.5, 0.25)
                    move_line(all_degrees, clientID, list_joints)

                    time.sleep(1)
                    move_home(clientID, list_joints)
                    object_grabbed = False

pygame.quit()