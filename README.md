# tr1-controller-demo
This repository contains code for running a simple controller demo on the Slate TR1. The demo allows the user to control all actuators on the robot using the Xbox controller included with the TR1.

## How to use
The default, starting mode is navigation. In this mode, you may use the joysticks to drive the base. The left joystick controls translation along the ground, and the right joystick controls rotation.

To change to manipulation mode, press 'B' on the controller.

## Upstart service
The program is installed as an upstart service that is located at `/etc/init/controller-demo.conf` and will execute on boot. In order to keep the service from starting on boot, we recommend you comment out the line with the `exec` statement as follows:
```bash
start on runlevel [2345]
stop on runlevel [!2345]
# exec /home/ubuntu/Documents/Github/tr1-controller-demo/sample.py
```
You may also stop the service at any time by entering `/etc/init/controller-demo.conf stop` and start the service by entering `/etc/init/controller-demo.conf start`.
