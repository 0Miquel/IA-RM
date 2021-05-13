import os
from flask import Flask, send_file, jsonify, request,send_from_directory, session
from flask_session import Session
from flask_cors import CORS
import json
import sim
from visualize_fun import *
from coppelia_fun import *
from movement_fun import *

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

    content = request.get_json()
    resposta = content['coppeliaid']
    # *************************************************************

    port = int(resposta)
    sim.simxFinish(-1)  # just in case, close all opened connections
    clientID = sim.simxStart('127.0.0.1', port, True, True, 1000, 5)  # Conectarse
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

    response = jsonify(res="notok")
    content = request.get_json()
    x = int(content['x'])
    y = int(content['y'])
    # *************************************************************

    print(x, y)
    image = get_image(clientID, sensorHandle)
    n_objects, im_labels = get_objects(image)
    if im_labels[y, x] != 0:

        object_label = im_labels[y, x]
        yf, xf, orientation = get_centroids_orientation(object_label, im_labels)
        xf = np.around(0.5 - xf * 0.5 / 512, 3)
        yf = np.around(0.5 - yf * 0.5 / 512, 3)
        print(f"x = {xf}, y = {yf}, orientation = {orientation}, object_label = {object_label}")

        correction_degree, reachable = movement_sequenceVertical(xf, yf, 0.1, list_joints,
                                                                 clientID)
        if reachable:
            response = jsonify(res="ok")
            angle0 = alignGrip(clientID, xf, yf, joint4, 0)
            move_joint5(clientID, joint5, orientation, correction_degree)
            for z in range(9, 1, -1):
                zf = z
                sensor_distance, object_handler = get_sensor_distance(clientID, psensor)
                if sensor_distance < 0.03:
                    break
                _, reachable = movement_sequenceVertical(xf, yf, z * 0.01, list_joints, clientID)
                angle0 = alignGrip(clientID, xf, yf, joint4, angle0)
            gripper(clientID, 1, object_handler)


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

    response = jsonify(res="notok")
    content = request.get_json()
    x = int(content['x'])
    y = int(content['y'])
    #*************************************************************

    _, reachable = movement_sequenceVertical(xf, yf, 0.2, list_joints, clientID)
    xf = np.around(0.5 - x * 0.5 / 512, 3)
    yf = np.around(0.5 - y * 0.5 / 512, 3)
    print(f"x = {xf}, y = {yf}")
    _, reachable = movement_sequenceVertical(xf, yf, 0.2, list_joints, clientID)
    if reachable:
        response = jsonify(res="ok")
        angle0 = alignGrip(clientID, xf, yf, joint4, angle0)
        for z in range(19, session["zf"], -1):
            _, reachable = movement_sequenceVertical(xf, yf, z * 0.01, list_joints, clientID)
            angle0 = alignGrip(clientID, xf, yf, joint4, angle0)
        gripper(clientID, 0, object_handler)
        move_home(clientID, list_joints)

    # *************************************************************
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

if __name__ == '__main__':

    app.run()

