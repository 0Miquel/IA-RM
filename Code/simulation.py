import pygame
from visualize_fun import *
from coppelia_fun import *
from movement_fun import *


clientID = connect(19999)
grip, joint1, joint2, joint3, joint4, joint5, dummy, sensorHandle, psensor = get_ids(clientID)
list_joints = [joint1, joint2, joint3, joint4]

pygame.init()

screen = pygame.display.set_mode((512, 512))
pygame.display.set_caption('IA-RM')
object_grabbed = False
running = True

while running:
    image = get_image(clientID, sensorHandle)

    surface = pygame.surfarray.make_surface(image)
    screen.blit(surface, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONUP:
            y, x = pygame.mouse.get_pos()
            print(y,x)
            n_objects, im_labels = get_objects(image)
            if im_labels[y, x] != 0 and not object_grabbed:
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
                xf = np.around(0.5 - x * 0.5 / 512, 3)
                yf = np.around(0.5 - y * 0.5 / 512, 3)
                print(f"x = {xf}, y = {yf}")
                correction_degree, reachable = movement_sequence(xf, yf, 0.25, list_joints, clientID)

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

    pygame.display.update()

pygame.quit()