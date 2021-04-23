import pygame
import time
from visualize_fun import *
from coppelia_fun import *
from movement_fun import *
from matplotlib import pyplot as plt
import cv2
import math

clientID = connect(19999)
grip, joint1, joint2, joint3, joint4, joint5, dummy, sensorHandle = get_ids(clientID)

pygame.init()

screen = pygame.display.set_mode((512, 512))
pygame.display.set_caption('IA-RM')
object_grabbed = False
running = True

while running:
    image = get_image(clientID, sensorHandle)
    img_GRAY = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    ret, thresh = cv2.threshold(img_GRAY,150,255,cv2.THRESH_BINARY)
    image = pygame.surfarray.make_surface(image)
    screen.blit(image, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONUP:
            y, x = pygame.mouse.get_pos()
            if thresh[y, x] == 0 and not object_grabbed:
                detector=cv2.SimpleBlobDetector_create() #Version antigua !!
                keypoints=detector.detect(thresh)
                yf, xf = get_nearest_keyPoint(keypoints, x, y)
                x = np.around(0.5 - xf * 0.5 / 512, 3)
                y = np.around(0.5 - yf * 0.5 / 512, 3)
                print(f"x = {x}, y = {y}")

                list_joints = [joint1, joint2, joint3, joint4]
                movement_sequence(x, y, 0.2, list_joints, clientID, 0)
                movement_sequence(x, y, 0.02, list_joints, clientID, 1)
                object_grabbed = True
            elif object_grabbed:
                x = np.around(0.5 - x * 0.5 / 512, 3)
                y = np.around(0.5 - y * 0.5 / 512, 3)
                movement_sequence(x, y, 0.2, list_joints, clientID, 0)
                move_home(clientID, list_joints)
                object_grabbed = False

    pygame.display.update()

pygame.quit()