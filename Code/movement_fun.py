import math
import numpy as np
import sim          # librería para conectar con CoppeliaSim
import sympy as sp  # librería para cálculo simbólico
import time
from coppelia_fun import *

def inverse_kinematics(x,y,z):
    """
    Calcula la cinemática inversa del robot, orientando la pinza hacia abajo
    :param x: coordenada x donde moverse
    :param y: coordenada y donde moverse
    :param z: coordenada z donde moverse
    :return: lista de grados calculada y si es posible moverse a esa posición
    """
    cabGrados = 90
    b = 0.3  # longitud de brazo mm
    ab = 0.3  # longitud de antebrazo mm
    m = 0.1 + 0.145  # longitud de muñequilla mm + pinza
    H = 0.2  # altura de base mm
    reachable = True
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
        reachable = False

    return [Axis1Grados, Axis2Grados, Axis3Grados, Axis4Grados], reachable

def sort_degrees(degrees, joints):
    """
    Ordenación de los grados de manera que produzca un movimiento sin peligro
    :param degrees: lista de los grados a ordenar
    :param joints: lista de joints a los que se asocia cada grado
    :return: lista de grados ordenada de mayor a menor junto a su joint
    """
    sorted_degrees = sorted(zip(degrees,joints), key=lambda x: x[0], reverse=True)
    return sorted_degrees

def move_to(clientID, list_grados):
    """
    Movimiento según los grados que se determinen
    :param clientID: Coppelia ID
    :param list_grados: lista de grados a moverse
    :return:
    """
    for grados, joint in list_grados:
        retCode = sim.simxSetJointTargetPosition(clientID, joint, grados * np.pi / 180, sim.simx_opmode_oneshot)

def move_home(clientID, list_joints):
    """
    Retorno del robot a la posición home
    :param clientID: Coppelia ID
    :param list_joints: lista de joints a mover
    :return:
    """
    joint1, joint2, joint3, joint4 = list_joints
    retCode = sim.simxSetJointTargetPosition(clientID, joint3, 0 * np.pi / 180, sim.simx_opmode_oneshot)
    time.sleep(1)
    retCode = sim.simxSetJointTargetPosition(clientID, joint1, 0 * np.pi / 180, sim.simx_opmode_oneshot)
    time.sleep(1)
    retCode = sim.simxSetJointTargetPosition(clientID, joint2, 180 * np.pi / 180, sim.simx_opmode_oneshot)
    time.sleep(1)
    retCode = sim.simxSetJointTargetPosition(clientID, joint4, 0 * np.pi / 180, sim.simx_opmode_oneshot)

def movement_sequence(x, y, z, list_joints, clientID):
    """
    Movimiento a una posición
    :param x: coordenada x donde moverse
    :param y: coordenada y donde moverse
    :param z: coordenada z donde moverse
    :param list_joints: lista de joints a mover
    :param clientID: Coppelia ID
    :return: angulo de correción para la orientación y si la posición és accesible
    """
    list_degrees, reachable = inverse_kinematics(x, y, z)
    correction_degree = list_degrees[0]
    sorted_degrees = sort_degrees(list_degrees, list_joints) #list of sorted degrees with its joint
    if reachable:
        move_to(clientID, sorted_degrees)
    return correction_degree, reachable

def move_joint5(clientID, joint5, orientation, correction_degree):
    """
    Orientación de la pinza
    :param clientID: Coppelia ID
    :param joint5: joint a orientar
    :param orientation: angulo a rotar
    :param correction_degree: angulo a corregir debido a la rotación de la base
    :return:
    """
    retCode = sim.simxSetJointTargetPosition(clientID, joint5,(90*np.pi/180)-orientation-(correction_degree*np.pi/180), sim.simx_opmode_oneshot)

def line(x,y,z):
    """
    Cálculo del movimiento lineal
    :param x: coordenada x donde moverse
    :param y: coordenada x donde moverse
    :param z: coordenada x donde moverse
    :return: lista de angulos a reproducir para conseguir el movimiento lineal
    """
    all_degrees = []
    for zi in range(int(z*100), 1, -1):
        list_degrees, reachable = inverse_kinematics(x, y, zi*0.01)
        all_degrees.append(list_degrees)
    return all_degrees

def line_up(x,y,z,zo):
    """
    Cálculo del movimiento lineal hacia arriba
    :param x: coordenada x donde moverse
    :param y: coordenada y donde moverse
    :param z: coordenada z donde empieza la linea
    :param zo: coordenada z donde acaba la linea
    :return: lista de angulos a reproducir para conseguir el movimiento lineal
    """
    all_degrees = []
    for zi in range(int(z * 100), int(zo * 100), 1):
        list_degrees, reachable = inverse_kinematics(x, y, zi * 0.01)
        all_degrees.append(list_degrees)
    return all_degrees

def line_down(x,y,z,zo):
    """
    Cálculo del movimiento lineal hacia abajo
    :param x: coordenada x donde moverse
    :param y: coordenada y donde moverse
    :param z: coordenada z donde empieza la linea
    :param zo: coordenada z donde acaba la linea
    :return: lista de angulos a reproducir para conseguir el movimiento lineal
    """
    all_degrees = []
    for zi in range(int(z*100), int(zo * 100), -1):
        list_degrees, reachable = inverse_kinematics(x, y, zi * 0.01)
        all_degrees.append(list_degrees)
    return all_degrees

def move_line(all_degrees, clientID, list_joints):
    """
    Realiza un movimiento lineal
    :param all_degrees: lista de ángulos a reproducir
    :param clientID: Coppelia ID
    :param list_joints: lista de joints a mover
    :return:
    """
    for degrees in all_degrees:
        retCode = sim.simxSetJointTargetPosition(clientID, list_joints[1], degrees[1] * np.pi / 180, sim.simx_opmode_oneshot)
        retCode = sim.simxSetJointTargetPosition(clientID, list_joints[2], degrees[2] * np.pi / 180, sim.simx_opmode_oneshot)
        retCode = sim.simxSetJointTargetPosition(clientID, list_joints[3], degrees[3] * np.pi/ 180, sim.simx_opmode_oneshot)


def grab_object(all_degrees, clientID, list_joints, psensor):
    """
    Realiza un movimiento lineal para agarrar un objeto
    :param all_degrees: lista de ángulos a reproducir
    :param clientID: Coppelia ID
    :param list_joints: lista de joints a mover
    :param psensor: ID del sensor ultrasonidos
    :return: ID del objeto a agarrar y altura a la que se encuentra el objeto
    """
    object_handler = -1
    for degrees in all_degrees:
        retCode = sim.simxSetJointTargetPosition(clientID, list_joints[1], degrees[1] * np.pi / 180, sim.simx_opmode_oneshot)
        retCode = sim.simxSetJointTargetPosition(clientID, list_joints[2], degrees[2] * np.pi / 180, sim.simx_opmode_oneshot)
        retCode = sim.simxSetJointTargetPosition(clientID, list_joints[3], degrees[3] * np.pi/ 180, sim.simx_opmode_oneshot)
        sensor_distance, object_handler = get_sensor_distance(clientID, psensor)
        if sensor_distance < 0.03:
            break

    retCode, Dummy = sim.simxGetObjectHandle(clientID, 'Dummy', sim.simx_opmode_blocking)
    retCode, pos = sim.simxGetObjectPosition(clientID, Dummy, -1, sim.simx_opmode_blocking)
    return object_handler, pos[2]