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

    return Axis1Grados, Axis2Grados, Axis3Grados, Axis4Grados

def sort_degrees(Axis1Grados, Axis2Grados, Axis3Grados, Axis4Grados, joint1, joint2, joint3, joint4):
    list_grados = [(Axis1Grados, joint1), (Axis2Grados, joint2), (Axis3Grados, joint3), (Axis4Grados, joint4)]
    list_grados = sorted(list_grados, key=lambda x: x[0], reverse=True)
    return list_grados

def move_to(clientID, list_grados):
    for grados, joint in list_grados:
        retCode = sim.simxSetJointTargetPosition(clientID, joint, grados * np.pi / 180, sim.simx_opmode_oneshot)
        time.sleep(1)

def move_home(clientID, joint1, joint2, joint3, joint4):
    retCode = sim.simxSetJointTargetPosition(clientID, joint3, 0 * np.pi / 180, sim.simx_opmode_oneshot)
    time.sleep(1)
    retCode = sim.simxSetJointTargetPosition(clientID, joint1, 0 * np.pi / 180, sim.simx_opmode_oneshot)
    time.sleep(1)
    retCode = sim.simxSetJointTargetPosition(clientID, joint2, 180 * np.pi / 180, sim.simx_opmode_oneshot)
    time.sleep(1)
    retCode = sim.simxSetJointTargetPosition(clientID, joint4, 0 * np.pi / 180, sim.simx_opmode_oneshot)

def movement_sequence(x, y, z, joint1, joint2, joint3, joint4, clientID, grip):
    Axis1Grados, Axis2Grados, Axis3Grados, Axis4Grados = inverse_kinematics(x, y, z)
    sorted_degrees = sort_degrees(Axis1Grados, Axis2Grados, Axis3Grados, Axis4Grados, joint1, joint2, joint3, joint4)
    move_to(clientID, sorted_degrees)
    time.sleep(1)
    gripper(clientID, grip)
    time.sleep(1)