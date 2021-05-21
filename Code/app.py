from visualize_fun import *
import torch, torchvision
predictor = build_predictor()
from flask import Flask, send_file, jsonify, request,send_from_directory, session
from flask_session import Session
from flask_cors import CORS
import json
import sim
from visualize_fun import *
from coppelia_fun import *
from movement_fun import *
from werkzeug.serving import WSGIRequestHandler
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"


torch.cuda.empty_cache()


app = Flask(__name__)
app.secret_key = 'abc'
CORS(app)

clientID = 0
grip = 0
joint1 = 0
joint2 = 0
joint3 = 0
joint4 = 0
joint5 = 0
dummy = 0
sensorHandle = 0
psensor = 0
list_joints = 0
zf = 0
xf = 0
yf = 0
object_handler = 0
angle0 = 0
object_grabbed = False
outputs = 0


@app.route('/coppelia', methods=['GET','POST'])
def hello_world():
    global clientID
    global grip
    global joint1
    global joint2
    global joint3
    global joint4
    global joint5
    global dummy
    global dummy
    global sensorHandle
    global psensor
    global list_joints
    global predictor
    content = request.get_json()
    resposta = content['coppeliaid']
    # *************************************************************

    port = int(resposta)
    sim.simxFinish(-1)  # just in case, close all opened connections
    clientID = sim.simxStart('127.0.0.1', port, True, True, 1000, 5)  # Conectarse
    #predictor =
    if clientID == 0:

        print("conectado a", port)
        response = jsonify(res="ok")
    else:
        response = jsonify(res="notok")
        print("no se pudo conectar")
    grip, joint1, joint2, joint3, joint4, joint5, dummy, sensorHandle, psensor = get_ids(clientID)
    list_joints = [joint1, joint2, joint3, joint4]

    # *************************************************************
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route('/getObject.png')
def image():
    global clientID
    global sensorHandle

    image = get_image(clientID,sensorHandle)
    directory = r'O:/Escriptori/RLP/Flask'
    os.chdir(directory)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    cv2.imwrite("image.png", image)
    return send_file('image.png', mimetype='image/png')

@app.route('/getObject', methods=['GET','POST'])
def getObject():
    global clientID
    global grip
    global joint1
    global joint2
    global joint3
    global joint4
    global joint5
    global dummy
    global dummy
    global sensorHandle
    global psensor
    global list_joints
    global zf
    global xf
    global yf
    global object_handler
    global angle0
    global object_grabbed
    retCode, leftShoulder = sim.simxGetObjectHandle(clientID, 'Bill_leftShoulderJoint', sim.simx_opmode_blocking)
    retCode, leftElbow = sim.simxGetObjectHandle(clientID, 'Bill_leftElbowJoint', sim.simx_opmode_blocking)
    retCode, dummyMa = sim.simxGetObjectHandle(clientID, 'Dummy_MaBill', sim.simx_opmode_blocking)
    retCode, attachBill = sim.simxGetObjectHandle(clientID, 'attachPointBill', sim.simx_opmode_blocking)
    retCode, attach = sim.simxGetObjectHandle(clientID, 'ROBOTIQ_85_attachPoint', sim.simx_opmode_blocking)

    response = jsonify(res="notok")
    content = request.get_json()
    x = int(content['y'])
    y = int(content['x'])
    # *************************************************************

    print(x, y)
    image = get_image(clientID, sensorHandle)
    n_objects, im_labels = get_objects(image)
    if im_labels[y, x] != 0 and not object_grabbed:
        object_label = im_labels[y, x]
        y, x, orientation = get_centroids_orientation(object_label, im_labels)
        xf = np.around(0.5 - x * 0.5 / 512, 3)
        yf = np.around(0.5 - y * 0.5 / 512, 3)
        print(f"x = {xf}, y = {yf}, orientation = {orientation}")
        correction_degree, reachable = movement_sequence(xf, yf, 0.25, list_joints, clientID)

        if reachable:
            response = jsonify(res="ok")
            time.sleep(1)
            move_joint5(clientID, joint5, orientation, correction_degree)

            time.sleep(1)
            all_degrees = line(xf, yf, 0.25)
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
                res, retInts, retFloats, retStrings, retBuffer = sim.simxCallScriptFunction(clientID, "ROBOTIQ_85",
                                                                                            sim.sim_scripttype_childscript,
                                                                                            "gripper", [0], [], [], "",
                                                                                            sim.simx_opmode_blocking)

                time.sleep(1)
                all_degrees = line_up(xb, yb, zb, 0.25)
                move_line(all_degrees, clientID, list_joints)

                time.sleep(1)
                move_home(clientID, list_joints)
                object_grabbed = True


    #*************************************************************
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/placeObject', methods=['GET','POST'])
def placeObject():
    global clientID
    global grip
    global joint1
    global joint2
    global joint3
    global joint4
    global joint5
    global dummy
    global dummy
    global sensorHandle
    global psensor
    global list_joints
    global zf
    global xf
    global yf
    global object_handler
    global angle0
    global object_grabbed
    retCode, leftShoulder = sim.simxGetObjectHandle(clientID, 'Bill_leftShoulderJoint', sim.simx_opmode_blocking)
    retCode, leftElbow = sim.simxGetObjectHandle(clientID, 'Bill_leftElbowJoint', sim.simx_opmode_blocking)
    retCode, dummyMa = sim.simxGetObjectHandle(clientID, 'Dummy_MaBill', sim.simx_opmode_blocking)
    retCode, attachBill = sim.simxGetObjectHandle(clientID, 'attachPointBill', sim.simx_opmode_blocking)
    retCode, attach = sim.simxGetObjectHandle(clientID, 'ROBOTIQ_85_attachPoint', sim.simx_opmode_blocking)
    response = jsonify(res="notok")
    content = request.get_json()
    x = int(content['y'])
    y = int(content['x'])
    #*************************************************************

    xf = np.around(0.5 - x * 0.5 / 512, 3)
    yf = np.around(0.5 - y * 0.5 / 512, 3)
    print(f"x = {xf}, y = {yf}")
    retCode, pos = sim.simxGetObjectPosition(clientID, dummyMa, -1, sim.simx_opmode_blocking)
    correction_degree, reachable = movement_sequence(pos[0], pos[1], 0.3, list_joints, clientID)
    if reachable:
        response = jsonify(res="ok")
        time.sleep(1)
        all_degrees = line_down(pos[0], pos[1], 0.3, pos[2] - 0.5)
        move_line(all_degrees, clientID, list_joints)

        time.sleep(1)
        sim.simxSetObjectParent(clientID, object_handler, attach, True, sim.simx_opmode_oneshot)
        time.sleep(1)
        res, retInts, retFloats, retStrings, retBuffer = sim.simxCallScriptFunction(clientID, "ROBOTIQ_85",
                                                                                    sim.sim_scripttype_childscript,
                                                                                    "gripper", [1], [], [], "",
                                                                                    sim.simx_opmode_blocking)
        time.sleep(1)
        all_degrees = line_up(pos[0], pos[1], pos[2] - 0.5, 0.3)
        move_line(all_degrees, clientID, list_joints)
        time.sleep(2)
        _, reachable = movement_sequence(xf, yf, 0.25, list_joints, clientID)

        time.sleep(2)
        all_degrees = line_down(xf, yf, 0.25, zf - 0.5)
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

    # *************************************************************
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/listObjects', methods=['GET','POST'])
def listObject():
    global outputs
    global predictor
    global clientID
    global  sensorHandle
    image = get_image(clientID, sensorHandle)
    outputs = predict_image(image, predictor)
    dict_objects2 = {0: "apple", 1: "banana", 2: "bluepills", 3: "bluepurplepill", 4: "glass", 5: "greenblackpills",
                     6: "orange", 7: "redpills", 8: "tv controller"}
    objects_list = get_objects_list(outputs, dict_objects2)
    llista = {'list': objects_list}
    return json.dumps(llista)

@app.route('/listObjectSend', methods=['GET','POST'])
def listObjectSend():
    global outputs
    global clientID
    global grip
    global joint1
    global joint2
    global joint3
    global joint4
    global joint5
    global dummy
    global dummy
    global sensorHandle
    global psensor
    global list_joints
    global zf
    global xf
    global yf
    global object_handler
    global angle0
    global object_grabbed
    global clientID
    global sensorHandle
    retCode, leftShoulder = sim.simxGetObjectHandle(clientID, 'Bill_leftShoulderJoint', sim.simx_opmode_blocking)
    retCode, leftElbow = sim.simxGetObjectHandle(clientID, 'Bill_leftElbowJoint', sim.simx_opmode_blocking)
    retCode, dummyMa = sim.simxGetObjectHandle(clientID, 'Dummy_MaBill', sim.simx_opmode_blocking)
    retCode, attachBill = sim.simxGetObjectHandle(clientID, 'attachPointBill', sim.simx_opmode_blocking)
    retCode, attach = sim.simxGetObjectHandle(clientID, 'ROBOTIQ_85_attachPoint', sim.simx_opmode_blocking)
    image = get_image(clientID, sensorHandle)

    response = jsonify(res="notok")
    content = request.get_json()
    object = content['object']

    dict_objects = {"apple": 0, "banana": 1, "bluepills": 2, "bluepurplepill": 3, "glass": 4, "greenblackpills": 5,
                    "orange": 6, "redpills": 7, "tv controller": 8}
    y, x = get_object_n(outputs, dict_objects[object])

    n_objects, im_labels = get_objects(image)

    object_label = im_labels[y, x]
    y, x, orientation = get_centroids_orientation(object_label, im_labels)
    xf = np.around(0.5 - x * 0.5 / 512, 3)
    yf = np.around(0.5 - y * 0.5 / 512, 3)
    print(f"x = {xf}, y = {yf}, orientation = {orientation}")
    correction_degree, reachable = movement_sequence(xf, yf, 0.25, list_joints, clientID)

    if reachable:
        response = jsonify(res="ok")
        time.sleep(1)
        move_joint5(clientID, joint5, orientation, correction_degree)

        time.sleep(1)
        all_degrees = line(xf, yf, 0.25)
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
            retCode = sim.simxSetJointTargetPosition(clientID, leftShoulder, 5 * np.pi / 180, sim.simx_opmode_oneshot)
            retCode = sim.simxSetJointTargetPosition(clientID, leftElbow, -55 * np.pi / 180, sim.simx_opmode_oneshot)
            time.sleep(1)
            sim.simxSetObjectParent(clientID, object_handler, attachBill, True, sim.simx_opmode_oneshot)
            time.sleep(1)
            res, retInts, retFloats, retStrings, retBuffer = sim.simxCallScriptFunction(clientID, "ROBOTIQ_85",
                                                                                        sim.sim_scripttype_childscript,
                                                                                        "gripper", [0], [], [], "",
                                                                                        sim.simx_opmode_blocking)

            time.sleep(1)
            all_degrees = line_up(xb, yb, zb, 0.25)
            move_line(all_degrees, clientID, list_joints)

            time.sleep(1)
            move_home(clientID, list_joints)
            object_grabbed = True

    return response

@app.route('/objectGrabbed', methods=['GET', 'POST'])
def objectGrabbed():
    global object_grabbed
    if(object_grabbed):
        response = jsonify(res="grabbed")
    else:
        response = jsonify(res="notgrabbed")

    return response

if __name__ == '__main__':
    WSGIRequestHandler.protocol_version = "HTTP/1.1"
    app.run()


