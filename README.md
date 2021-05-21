# IA-RM
### Anthropomorphic arm for assistance purposes. Controlled via a mobile app, the user can select objects to pick and where to place it.

![complet](https://user-images.githubusercontent.com/49688038/116916362-83492400-ac4d-11eb-8e5a-c14069ae2904.PNG)
### Robotics, language and planification project from Universitat Autònoma de Barcelona
#### Members:
- Miquel Romero Blanch
- Gerard Graugés Bellver
- Guillem
- Oriol Graupera Serra


#
## Hardware scheme
List of used components:
- I2C controller: Connected to the servos 
- Raspberry Cam: Connected to the raspberry pi
- Raspberry pi: Connected to the I2C controller, a battery via USB and the camera.
- Battery: It provides energy to the I2C controller.
- USB battery:  It provides energy to the Raspberry PI
- Servos: Connected to the I2C controller. The servos provide the kinematics of the arm.
- Ultrasonic sensors: Connected to the I2C controller. The sensor provides the height of the object.

![hardware](https://user-images.githubusercontent.com/48658941/119167890-9edf6780-ba60-11eb-9810-899a9305d32a.jpg)



## Software achitecture
![software](https://user-images.githubusercontent.com/48658941/119168001-bdddf980-ba60-11eb-8015-e206ffd7bcc7.jpg)

All the software is controlled via Python code, which is compatible with Raspberry Pi.

### Object detection
The model is able to detect the following objects:
- Banana
- Orange
- Apple
- Glass
- TV Command

Additionally, it is also able to detect glasses with different types of pills.

Two different models have been tested for object detection, YOLOv5 and Mask R-CNN provided by [detectron2](https://github.com/facebookresearch/detectron2). As a result, it has been decided to use YOLOv5 which performs better in the pills recognition problem.

![yolov5](https://user-images.githubusercontent.com/48658941/119170678-e6b3be00-ba63-11eb-9f0f-37ebf7adf330.jpg)

PONER GIF DE ESTO

PONER LINK AL COLAB O ALGO

### Mobile application
Mobile application to select the object that will be moved to a specified area. It also gets feedback about the objects in the work area and the robot status.

To develop the mobile App, it is used a framework called Flutter which works with dart programming language. Additionally, to communicate the App and the Python code that controls the robot it is used the framework Flask.

![app1](https://user-images.githubusercontent.com/48658941/119168193-f087f200-ba60-11eb-81bc-c63d2c1350ec.jpg)

![app2](https://user-images.githubusercontent.com/48658941/119168302-0eeded80-ba61-11eb-98fb-54403e54f49f.jpg)

## Video demonstration
