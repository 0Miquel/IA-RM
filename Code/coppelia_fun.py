import sim          # librería para conectar con CoppeliaSim
import sympy as sp  # librería para cálculo simbólico

def connect(port):
    """
    Realiza la connexión a la API de Coppelia
    :param port:
    :return: ID del cliente de la API de Coppelia
    """
    sim.simxFinish(-1) # just in case, close all opened connections
    clientID=sim.simxStart('127.0.0.1',port,True,True,2000,5) # Conectarse
    if clientID == 0: print("conectado a", port)
    else: print("no se pudo conectar")
    return clientID


def gripper(clientID, val):
    """
    Acciona el efector de la pinza remotamente
    :param clientID: Coppelia ID
    :param val: Acción a realizar sobre la pinza, 0 = abrir, 1 = cerrar
    :return: Codigo del resultado, 0 = satisfactorio
    """
    res,retInts,retFloats,retStrings,retBuffer=sim.simxCallScriptFunction(clientID, "ROBOTIQ_85", sim.sim_scripttype_childscript,"gripper",[val],[],[],"", sim.simx_opmode_blocking)
    return res

def get_ids(clientID):
    """
    Devuelve los IDs que encontramos en nuestra escena de Coppelia
    :param clientID: Coppelia ID
    :return: IDs de cada uno de los handlers que encontramos en nuestra escena
    """
    retCode, sensorHandle = sim.simxGetObjectHandle(clientID, 'Vision_sensor', sim.simx_opmode_blocking)
    retCode, grip = sim.simxGetObjectHandle(clientID, 'ROBOTIQ_85', sim.simx_opmode_blocking)
    retCode, joint1 = sim.simxGetObjectHandle(clientID, 'Joint1', sim.simx_opmode_blocking)
    retCode, joint2 = sim.simxGetObjectHandle(clientID, 'Joint2', sim.simx_opmode_blocking)
    retCode, joint3 = sim.simxGetObjectHandle(clientID, 'Joint3', sim.simx_opmode_blocking)
    retCode, joint4 = sim.simxGetObjectHandle(clientID, 'Joint4', sim.simx_opmode_blocking)
    retCode, joint5 = sim.simxGetObjectHandle(clientID, 'Joint5', sim.simx_opmode_blocking)
    retCode, dummy = sim.simxGetObjectHandle(clientID, 'Dummy', sim.simx_opmode_blocking)

    return grip, joint1, joint2, joint3, joint4, joint5, dummy, sensorHandle