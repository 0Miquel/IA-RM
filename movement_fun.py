import math
import numpy as np
import sim          # librería para conectar con CoppeliaSim
import sympy as sp  # librería para cálculo simbólico
import time
from coppelia_fun import *




def inverse_kinematics(x,y,z):
    cabGrados = 0
    b = 0.2  # longitud de brazo mm
    ab = 0.2  # longitud de antebrazo mm
    m = 0.1 + 0.145  # longitud de muñequilla mm + pinza
    H = 0.2  # altura de base mm

    try:
        cabRAD = cabGrados * np.pi / 180
        Axis1 = math.atan2(y, x)
        M = math.sqrt(pow(x, 2) + pow(y, 2))
        xprima = M
        yprima = z
        Afx = math.cos(cabRAD) * m

        B = xprima - Afx
        Afy = math.sin(cabRAD) * m
        A = yprima + Afy - H
        Hip = math.sqrt(pow(A, 2) + pow(B, 2))
        alfa = math.atan2(A, B)
        beta = math.acos((pow(b, 2) - pow(ab, 2) + pow(Hip, 2)) / (2 * b * Hip))
        Axis2 = alfa + beta
        gamma = math.acos((pow(b, 2) + pow(ab, 2) - pow(Hip, 2)) / (2 * b * ab))
        Axis3 = gamma
        Axis4 = 2 * np.pi - cabRAD - Axis2 - Axis3

        Axis1Grados = (Axis1 * 180 / np.pi)  # Giro base en Grados
        Axis2Grados = (90 - Axis2 * 180 / np.pi)  # Giro brazo en Grados
        Axis3Grados = (180 - Axis3 * 180 / np.pi)  # Giro antebrazo grados
        Axis4Grados = (180 - Axis4 * 180 / np.pi)  # Giro muñequilla grados

        Axis2Grados = 90 + abs(90 - Axis2Grados)
        Axis3Grados = -Axis3Grados
        Axis4Grados = -Axis4Grados
    except:
        print("Non reachable")
        Axis1Grados, Axis2Grados, Axis3Grados, Axis4Grados = 0, 180, 0, 0

    return [Axis1Grados, Axis2Grados, Axis3Grados, Axis4Grados]

def sort_degrees(degrees, joints):
    sorted_degrees = sorted(zip(degrees,joints), key=lambda x: x[0], reverse=True)
    return sorted_degrees

def move_to(clientID, list_grados):
    for grados, joint in list_grados:
        retCode = sim.simxSetJointTargetPosition(clientID, joint, grados * np.pi / 180, sim.simx_opmode_oneshot)
        time.sleep(1)

def move_home(clientID, list_joints):
    joint1, joint2, joint3, joint4 = list_joints
    retCode = sim.simxSetJointTargetPosition(clientID, joint3, 0 * np.pi / 180, sim.simx_opmode_oneshot)
    time.sleep(1)
    retCode = sim.simxSetJointTargetPosition(clientID, joint1, 0 * np.pi / 180, sim.simx_opmode_oneshot)
    time.sleep(1)
    retCode = sim.simxSetJointTargetPosition(clientID, joint2, 180 * np.pi / 180, sim.simx_opmode_oneshot)
    time.sleep(1)
    retCode = sim.simxSetJointTargetPosition(clientID, joint4, 0 * np.pi / 180, sim.simx_opmode_oneshot)

def movement_sequence(x, y, z, list_joints, clientID, grip):
    list_degrees = inverse_kinematics(x, y, z)
    sorted_degrees = sort_degrees(list_degrees, list_joints) #list of sorted degrees with its joint
    move_to(clientID, sorted_degrees)
    time.sleep(1)
    gripper(clientID, grip)
    time.sleep(1)


#vertical movement set

def inverse_kinematicsVertical(x,y,z):
    cabGrados = 0
    b = 0.2  # longitud de brazo mm
    ab = 0.2  # longitud de antebrazo mm
    m = 0.1 + 0.145  # longitud de muñequilla mm + pinza
    H = 0.2  # altura de base mm

    try:
        Axis1 = math.atan2(y, x)
        xprima = math.sqrt(pow(x, 2) + pow(y, 2))
        yprima = z
        B = xprima
        A = z - H + m; # Suma de la longitud de la muñequilla+pinza

        Hip = math.sqrt(pow(A, 2) + pow(B, 2))
        alfa = math.atan2(A, B)
        beta = math.acos((pow(b, 2) - pow(ab, 2) + pow(Hip, 2)) / (2 * b * Hip))
        Axis2 = alfa + beta
        gamma = math.acos((pow(b, 2) + pow(ab, 2) - pow(Hip, 2)) / (2 * b * ab))
        Axis3 = gamma

        Axis1Grados = (Axis1 * 180 / np.pi)  # Giro base en Grados
        Axis2Grados = (90 - Axis2 * 180 / np.pi)  # Giro brazo en Grados
        Axis3Grados = (180 - Axis3 * 180 / np.pi)  # Giro antebrazo grados

        Axis2Grados = 90 + abs(90 - Axis2Grados)
        Axis3Grados = -Axis3Grados
    except:
        print("Non reachable")
        Axis1Grados, Axis2Grados, Axis3Grados,  = 0, 180, 0

    return [Axis1Grados, Axis2Grados, Axis3Grados]

def movement_sequenceVertical(x, y, z, list_joints, clientID, grip, angle0, object_grabbed):
    list_degrees = inverse_kinematicsVertical(x, y, z)
    sorted_degrees = sort_degrees(list_degrees, list_joints[:-1]) #list of sorted degrees with its joint
    move_to(clientID, sorted_degrees)
    time.sleep(1)
    #mover joint4
    if (object_grabbed==False): # Alineamiento solo para coger el objeto
        angle1 = alingGrip(clientID, x,y)
        angle2 = angle0-angle1 #desde el angulo en el que estamos hasta el angulo que queremos (Provisional)
        if angle2>0:
            angle2 = -angle2 # queremos que elangulo siempre sea negativo (Provisional)
        retCode = sim.simxSetJointTargetPosition(clientID, list_joints[-1], angle2 * np.pi / 180, sim.simx_opmode_oneshot)
        time.sleep(1)
    gripper(clientID, grip)
    time.sleep(1)
    return angle1

def alingGrip(clientID, x, y):
    # Posicion keypoint
    x_k = x
    y_k = y

    retCode, Dummy = sim.simxGetObjectHandle(clientID, 'Dummy', sim.simx_opmode_blocking)
    retCode, pos = sim.simxGetObjectPosition(clientID, Dummy, -1, sim.simx_opmode_blocking) # Calculamos la posición del Dummy para la trigonometría
    print(pos)
    xD = pos[0]
    yD = pos[1]

    dist = math.sqrt(((x_k - xD) ** 2) + ((y_k - yD) ** 2))
    angle = math.sin(dist / 0.245) * 90 # distancia del Dummy hasta el Keypoint / distancia del joint hasta la pinza
    print(angle)

    return angle