from flask import Flask, send_file, jsonify, request,send_from_directory
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

@app.route('/coppelia', methods=['GET','POST'])
def hello_world():

    content = request.get_json()
    resposta = content['coppeliaid']

    if resposta == '19999':
        response = jsonify(res="ok")
    else:
        response = jsonify(res="notok")
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route('/getObject.png')
def image():
    return send_file('1.png', mimetype='image/png')

@app.route('/getObject')
def getObject():
    response = jsonify(res="ok")
    content = request.get_json()
    x = int(content['x'])
    y = int(content['y'])

    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/placeObject')
def placeObject():
    response = jsonify(res="ok")
    content = request.get_json()
    x = int(content['x'])
    y = int(content['y'])

    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

if __name__ == '__main__':
    app.run()

