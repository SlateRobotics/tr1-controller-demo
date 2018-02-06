#!/usr/bin/python 
import sys
import i2c_wrapper
import xbox_controller
import helper
import numpy as np
from time import sleep

sys.stdout.write("Program starting up...")

ADDRESS_BASE_MOTORS = 0x70
ADDRESS_TORSO_ACTUATOR = 0x71
ADDRESS_ARM_RIGHT_1 = 0x72
ADDRESS_ARM_RIGHT_2 = 0x73
ADDRESS_HEAD = 0x74

MODE_NAVIGATE = 0
MODE_MANIPULATE = 1
MODE_HEAD = 2

i2c = i2c_wrapper.i2c()
controller = xbox_controller.getController()
mode = MODE_NAVIGATE

servo1 = 55
servo2 = 5

def navigate():
	address = ADDRESS_BASE_MOTORS
	mode = 0

	leftStick = controller.leftStick()
	rightStickX = controller.rightStick()[0]
	motorValues = helper.getMotorValues(np.array(leftStick), rightStickX)

	total = abs(motorValues[0]) + abs(motorValues[1]) + abs(motorValues[2]) + abs(motorValues[3])
	if (total > 0):
		data = [1, int(abs(motorValues[0]) * 100), int(motorValues[0] < 0), 10]
		data.extend([2, int(abs(motorValues[1]) * 100), int(motorValues[1] < 0), 10])
		data.extend([3, int(abs(motorValues[2]) * 100), int(motorValues[2] < 0), 10])
		data.extend([4, int(abs(motorValues[3]) * 100), int(motorValues[3] < 0), 10])

		i2c.sendBlockData(address, mode, data)

def manipulate():
	address = ADDRESS_ARM_RIGHT_1
	address2 = ADDRESS_ARM_RIGHT_2
	mode = 0
	data = []
	data2 = []
	
	leftTrigger = controller.leftTrigger()
	rightTrigger = controller.rightTrigger()
	leftStick = controller.leftStick()
	rightStick = controller.rightStick()

	global servo1
	global servo2

        if (abs(leftStick[0]) > 0):
                data.extend([1, abs(int(leftStick[0] * 100)), int(leftStick[0] < 0), 10])
	else:
		data.extend([1, 0, 0, 10])

	if (abs(leftStick[1]) > 0):
		data.extend([2, abs(int(leftStick[1] * 100)), int(leftStick[1] < 0), 10])
	else:
		data.extend([2, 0, 0, 10])

        if (abs(rightStick[0]) > 0):
                data.extend([4, abs(int(rightStick[0] * 100)), int(rightStick[0] < 0), 10])
	else:
		data.extend([4, 0, 0, 10])

	if (abs(rightStick[1]) > 0):
		data.extend([3, abs(int(rightStick[1] * 100)), int(rightStick[1] > 0), 10])
	else:
		data.extend([3, 0, 0, 10])

	if (controller.dpadLeft()):
		data2.extend([1, 100, 0, 10])
	elif (controller.dpadRight()):
		data2.extend([1, 100, 1, 10])
	else:
		data2.extend([1, 0, 0, 10])

	if (controller.dpadUp()):
		data2.extend([2, 100, 0, 10])
	elif (controller.dpadDown()):
		data2.extend([2, 100, 1, 10])
	else:
		data2.extend([2, 0, 0, 10])

	if (controller.leftThumbstick()):
		if (leftTrigger > 0.5):
			setServo1(-5)
                	data2.extend([3, servo1, 0, 0])
	        elif (rightTrigger > 0.5):
			setServo1(5)
        	        data2.extend([3, servo1, 0, 0])
	else:
		if (leftTrigger > 0.5):
			setServo2(-10)
			data2.extend([4, servo2, 0, 0])
		elif (rightTrigger > 0.5):
			setServo2(10)
			data2.extend([4, servo2, 0, 0])


	i2c.sendBlockData(address, mode, data)
	i2c.sendBlockData(address2, mode, data2)

def setServo1(i):
	global servo1
	if (i < 5):
		if (servo1 > i):
			servo1 = servo1 + i
	else:
		if (servo1 < 180 - i):
			servo1 = servo1 + i

def setServo2(i):
	global servo2
        if (i < 5):   
                if (servo2 > i): 
                        servo2 = servo2 + i 
        else: 
                if (servo2 < 180 - i):
                        servo2 = servo2 + i

def actuateTorso():
	address = ADDRESS_TORSO_ACTUATOR
	mode = 0
	data = []

	if controller.rightBumper():
		data = [100, 0, 10]
	elif controller.leftBumper():
		data = [100, 1, 10]
	
	i2c.sendBlockData(address, mode, data)

def actuateHead():
	address = ADDRESS_HEAD
	mode = 0
	data = []

	if controller.dpadUp():
		data = [100, 1, 10]
	elif controller.dpadDown():
		data = [100, 0, 10]

	i2c.sendBlockData(address, mode, data)

def controlRobot():
	global mode
	if mode == MODE_NAVIGATE:
		navigate()
	elif mode == MODE_MANIPULATE:
		manipulate()
	elif mode == MODE_HEAD:
		actuateHead()

	actuateTorso()

def setMode():
	global mode
	if controller.A():
		mode = MODE_NAVIGATE
	elif controller.B():
		mode = MODE_MANIPULATE
	elif controller.Y():
		mode = MODE_HEAD

def modeToString():
	global mode
	if mode == MODE_NAVIGATE:
		return "Navigate  "
	elif mode == MODE_MANIPULATE:
		return "Manipulate"
	elif mode == MODE_HEAD:
		return "Head      "
		
sys.stdout.write("\n**********************************************")
sys.stdout.write("\n** Program Ready! Press Back button to exit **")
sys.stdout.write("\n**********************************************\n")

while not controller.Back():
	if controller.connected():
		setMode()
		controlRobot()
		sys.stdout.write("\rController connected, Mode: " + modeToString())
	else:
		sys.stdout.write("\rController disconnected                         ")

	sleep(0.050)
	sys.stdout.flush()

sys.stdout.write("\nBack button pressed. Exiting...\n")
controller.close()
