from flask import Flask, send_file, jsonify, request,send_from_directory, session
from flask_cors import CORS
from visualize_fun import *
from coppelia_fun import *
from movement_fun import *
import json

app = Flask(__name__)
CORS(app)

@app.route('/coppelia', methods=['GET','POST'])
def connection():

    content = request.get_json()
    resposta = content['coppeliaid']

    if resposta == '19999':
        response = jsonify(res="ok")
        clientID = connect(int(resposta))
        grip, joint1, joint2, joint3, joint4, joint5, dummy, sensorHandle, psensor = get_ids(clientID)
        list_joints = [joint1, joint2, joint3, joint4]
        session["clientID"] = clientID
        session["grip"] = grip
        session["joint1"] = joint1
        session["joint2"] = joint2
        session["joint3"] = joint3
        session["joint4"] = joint4
        session["joint5"] = joint5
        session["dummy"] = dummy
        session["sensorHandle"] = sensorHandle
        session["psensor"] = psensor
        session["list_joints"] = list_joints
    else:
        response = jsonify(res="notok")
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route('/getObject.png')
def image():
    image = get_image(session["clientID"], session["sensorHandle"])
    cv2.imwrite("image.png", image)
    return send_file('image.png', mimetype='image/png')

@app.route('/getObject')
def getObject():
    response = jsonify(res="notok")
    content = request.get_json()
    x = int(content['x'])
    y = int(content['y'])

    n_objects, im_labels = get_objects(image)
    if im_labels[y, x] != 0:

        object_label = im_labels[y, x]
        yf, xf, orientation = get_centroids_orientation(object_label, im_labels)
        xf = np.around(0.5 - xf * 0.5 / 512, 3)
        yf = np.around(0.5 - yf * 0.5 / 512, 3)
        print(f"x = {xf}, y = {yf}, orientation = {orientation}, object_label = {object_label}")

        correction_degree, reachable = movement_sequenceVertical(xf, yf, 0.1, session["list_joints"], session["clientID"])
        if reachable:
            response = jsonify(res="ok")
            angle0 = alignGrip(session["clientID"], xf, yf, session["joint4"], 0)
            move_joint5(session["clientID"], session["joint5"], orientation, correction_degree)
            for z in range(9, 1, -1):
                zf = z
                sensor_distance, object_handler = get_sensor_distance(session["clientID"], session["psensor"])
                if sensor_distance < 0.03:
                    break
                _, reachable = movement_sequenceVertical(xf, yf, z * 0.01, session["list_joints"], session["clientID"])
                angle0 = alignGrip(session["clientID"], xf, yf, session["joint4"], angle0)
            gripper(session["clientID"], 1, object_handler)

            session["zf"] = zf
            session["xf"] = xf
            session["yf"] = yf
            session["object_handler"] = object_handler
            session["angle0"] = angle0

    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/placeObject')
def placeObject():
    response = jsonify(res="notok")
    content = request.get_json()
    x = int(content['x'])
    y = int(content['y'])

    _, reachable = movement_sequenceVertical(session["xf"], session["yf"], 0.2, session["list_joints"], session["clientID"])
    xf = np.around(0.5 - x * 0.5 / 512, 3)
    yf = np.around(0.5 - y * 0.5 / 512, 3)
    print(f"x = {xf}, y = {yf}")
    _, reachable = movement_sequenceVertical(xf, yf, 0.2, session["list_joints"], session["clientID"])
    if reachable:
        response = jsonify(res="ok")
        angle0 = alignGrip(session["clientID"], xf, yf, session["joint4"], session["angle0"])
        for z in range(19, session["zf"], -1):
            _, reachable = movement_sequenceVertical(xf, yf, z * 0.01, session["list_joints"], session["clientID"])
            angle0 = alignGrip(session["clientID"], xf, yf, session["joint4"], angle0)
        gripper(session["clientID"], 0, session["object_handler"])
        move_home(session["clientID"], session["list_joints"])

    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

if __name__ == '__main__':
    app.run()

