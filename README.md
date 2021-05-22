# IA-RM
### Anthropomorphic arm for assistance purposes controlled via a mobile app and object recognition.

![robot](https://user-images.githubusercontent.com/48658941/119174514-f84b9480-ba68-11eb-8a75-8bf788b5b577.jpg)

### Robotics, language and planification project from Universitat Autònoma de Barcelona

#
## Hardware scheme
List of used components:
- I2C controller: Connected to the servos 
- Raspberry Cam: Connected to the raspberry pi
- Raspberry pi: Connected to the I2C controller, a battery via USB and the camera.
- Battery: It provides energy to the I2C controller.
- USB battery:  It provides energy to the Raspberry PI
- Servos: Connected to the I2C controller. The servos provide the kinematics of the arm.
- Ultrasonic sensors: Connected to the I2C controller. The sensor estimates the height of the object.

![hardware](https://user-images.githubusercontent.com/48658941/119167890-9edf6780-ba60-11eb-9810-899a9305d32a.jpg)



## Software achitecture
![Software Architecture](https://user-images.githubusercontent.com/48658941/119220540-528d3980-baeb-11eb-9890-4cf418c01c8d.jpg)

All the software is controlled via Python code, which is compatible with Raspberry Pi.

### Object recognition
The model is able to detect the following objects:
- Banana
- Orange
- Apple
- Glass
- TV Command

Additionally, it is also able to detect glasses with different types of pills.

Two different models have been tested for object detection, YOLOv5 and Mask R-CNN provided by [detectron2](https://github.com/facebookresearch/detectron2). As a result, it has been decided to use YOLOv5 which performs better in the pills recognition problem.

![yolov5](https://user-images.githubusercontent.com/48658941/119170678-e6b3be00-ba63-11eb-9f0f-37ebf7adf330.jpg)

Example of the ground truth vs our predictions:

<img src="https://user-images.githubusercontent.com/48658941/119219700-253e8c80-bae7-11eb-8121-5c54f2ace859.gif" width="500" height="500" />

PONER LINK AL COLAB O ALGO

### Mobile application
Mobile application to select the object that will be moved to a specified area. It also gets feedback about the objects in the work area and the robot status.

To develop the mobile App, it is used a framework called Flutter which works with dart programming language. Additionally, to communicate the App and the Python code that controls the robot it is used the framework Flask.

![app1](https://user-images.githubusercontent.com/48658941/119168193-f087f200-ba60-11eb-81bc-c63d2c1350ec.jpg)

![app2](https://user-images.githubusercontent.com/48658941/119168302-0eeded80-ba61-11eb-98fb-54403e54f49f.jpg)

### Kinematics
As it consists of a 5 axis robot which has a huge number of different solutions, it has been decided to develop a kinematics geometric approach instead of an algebraic approach which is also faster and it provides a better user experience.

Additionally, a linear movement has been developed so as to achieve a better and safer grasping using the line equation.


## Video demonstration

## Authors
- Miquel Romero Blanch
- Gerard Graugés Bellver
- Guillem Martínez Sánchez
- Oriol Graupera Serra
