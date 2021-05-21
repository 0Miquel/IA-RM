import pygame
from visualize_fun import *
from coppelia_fun import *
from movement_fun import *
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

clientID = connect(19999)
grip, joint1, joint2, joint3, joint4, joint5, dummy, sensorHandle, psensor = get_ids(clientID)
list_joints = [joint1, joint2, joint3, joint4]

retCode, leftShoulder = sim.simxGetObjectHandle(clientID, 'Bill_leftShoulderJoint', sim.simx_opmode_blocking)
retCode, leftElbow = sim.simxGetObjectHandle(clientID, 'Bill_leftElbowJoint', sim.simx_opmode_blocking)
retCode, dummyMa = sim.simxGetObjectHandle(clientID, 'Dummy_MaBill', sim.simx_opmode_blocking)
retCode, attachBill = sim.simxGetObjectHandle(clientID, 'attachPointBill', sim.simx_opmode_blocking)
retCode, attach = sim.simxGetObjectHandle(clientID, 'ROBOTIQ_85_attachPoint', sim.simx_opmode_blocking)
 

pygame.init()

screen = pygame.display.set_mode((512, 512))
pygame.display.set_caption('IA-RM')
object_grabbed = False
running = True
billHasObject = False

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


                    time.sleep(1)
                    #retCode, pos = sim.simxGetObjectPosition(clientID, dummyMa, -1, sim.simx_opmode_blocking)
                    xb = 0.44
                    yb = -0.24
                    zb = 0.17
                    print(f"x = {xf}, y = {yf}")
                    correction_degree, reachable = movement_sequence(xb, yb, zb, list_joints, clientID)
    
                    if reachable:
                        time.sleep(1)
                        retCode = sim.simxSetJointTargetPosition(clientID, leftShoulder, 5 * np.pi / 180,sim.simx_opmode_oneshot)
                        retCode = sim.simxSetJointTargetPosition(clientID, leftElbow, -55 * np.pi / 180,sim.simx_opmode_oneshot)
                        time.sleep(1)
                        sim.simxSetObjectParent(clientID, object_handler, attachBill, True, sim.simx_opmode_oneshot)
                        time.sleep(1)
                        res,retInts,retFloats,retStrings,retBuffer=sim.simxCallScriptFunction(clientID, "ROBOTIQ_85", sim.sim_scripttype_childscript,"gripper",[0],[],[],"", sim.simx_opmode_blocking)

                        time.sleep(1)
                        all_degrees = line_up(xb, yb, zb, 0.25)
                        move_line(all_degrees, clientID, list_joints)

                        time.sleep(1)
                        move_home(clientID, list_joints)
                        object_grabbed = True

            elif object_grabbed:
                xf = np.around(0.5 - x * 0.5 / 512, 3)
                yf = np.around(0.5 - y * 0.5 / 512, 3)
                        
                retCode, pos = sim.simxGetObjectPosition(clientID, dummyMa, -1, sim.simx_opmode_blocking)
                correction_degree, reachable = movement_sequence(pos[0],pos[1],0.3, list_joints, clientID)
                if reachable:
                    time.sleep(1)
                    all_degrees = line_down(pos[0],pos[1],0.3, pos[2] - 0.5 - 0.03)
                    move_line(all_degrees, clientID, list_joints)
        
                    time.sleep(1)
                    sim.simxSetObjectParent(clientID, object_handler, attach, True, sim.simx_opmode_oneshot)
                    time.sleep(1)
                    res,retInts,retFloats,retStrings,retBuffer=sim.simxCallScriptFunction(clientID, "ROBOTIQ_85", sim.sim_scripttype_childscript,"gripper",[1],[],[],"", sim.simx_opmode_blocking)
                    time.sleep(1)
                    all_degrees = line_up(pos[0],pos[1],pos[2] - 0.5, 0.3)
                    move_line(all_degrees, clientID, list_joints)
                    time.sleep(2)
                    _, reachable = movement_sequence(xf, yf, 0.25, list_joints, clientID)

                    time.sleep(2)
                    all_degrees = line_down(xf, yf, 0.25, zf-0.5)
                    move_line(all_degrees, clientID, list_joints)

                    time.sleep(2)
                    gripper(clientID, 0, object_handler)

                    time.sleep(2)
                    all_degrees = line_up(xf, yf, zf - 0.5, 0.25)
                    move_line(all_degrees, clientID, list_joints)

                    time.sleep(1)
                    move_home(clientID, list_joints)                   
                
                retCode = sim.simxSetJointTargetPosition(clientID, leftShoulder, 0 * np.pi / 180, sim.simx_opmode_oneshot)
                retCode = sim.simxSetJointTargetPosition(clientID, leftElbow, 0 * np.pi / 180, sim.simx_opmode_oneshot)
                
                object_grabbed = False
        

    pygame.display.update()

pygame.quit()