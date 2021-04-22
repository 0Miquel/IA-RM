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
running = True

while running:
    image = get_image(clientID, sensorHandle)
    
    img_GRAY = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    ret, thresh = cv2.threshold(img_GRAY,150,255,cv2.THRESH_BINARY)
    plt.imshow(thresh)
    image = pygame.surfarray.make_surface(image)
    
    screen.blit(image, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            y, x = pygame.mouse.get_pos()
            print(x,y)
            if thresh[y, x] == 0:
                detector=cv2.SimpleBlobDetector_create() #Verion antigua !!
                keypoints=detector.detect(thresh)
                
                for keyPoint in keypoints:
                    xi = np.around(keyPoint.pt[0],5)    
                    yi = np.around(keyPoint.pt[1],5)
                    si = np.around(keyPoint.size,5)
                    
                    print (xi,yi,si)
                                                
                x = np.around(0.5 - xi * 0.5 / 512, 3)
                y = np.around(0.5 - yi * 0.5 / 512, 3)
                print(f"x = {x}, y = {y}")
    
                Axis1Grados, Axis2Grados, Axis3Grados, Axis4Grados = inverse_kinematics(x, y, 0.2)
                sorted_degrees = sort_degrees(Axis1Grados, Axis2Grados, Axis3Grados, Axis4Grados, joint1, joint2, joint3, joint4)
                move_to(clientID, sorted_degrees)
                time.sleep(4)
                move_home(clientID, joint1, joint2, joint3, joint4)

    pygame.display.update()

pygame.quit()