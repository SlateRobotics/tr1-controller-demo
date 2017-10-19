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

i2c = i2c_wrapper.i2c()
controller = xbox_controller.getController()
mode = MODE_NAVIGATE

def navigate():
	address = ADDRESS_BASE_MOTORS
	mode = 0

	leftStick = controller.leftStick()
	rightStickX = controller.rightStick()[0]
	motorValues = helper.getMotorValues(np.array(leftStick), rightStickX)
	data = [1, int(abs(motorValues[0]) * 100), int(motorValues[0] < 0), 10]
	data.extend([2, int(abs(motorValues[1]) * 100), int(motorValues[1] < 0), 10])
	data.extend([3, int(abs(motorValues[2]) * 100), int(motorValues[2] < 0), 10])
	data.extend([4, int(abs(motorValues[3]) * 100), int(motorValues[3] < 0), 10])

	i2c.sendBlockData(address, mode, data)

def manipulate():
	address = ADDRESS_ARM_RIGHT_1
	mode = 0
	data = []
	
	leftStick = controller.leftStick()
	rightStick = controller.rightStick()

        if (abs(leftStick[0]) > 0.25):
                data.extend([1, abs(int(leftStick[0] * 100)), int(leftStick[0] < 0), 10])

	if (abs(leftStick[1]) > 0.25):
		data.extend([2, abs(int(leftStick[1] * 100)), int(leftStick[1] < 0), 10])

        if (abs(rightStick[0]) > 0.25):
                data.extend([4, abs(int(rightStick[0] * 100)), int(rightStick[0] < 0), 10])

	if (abs(rightStick[1]) > 0.25):
		data.extend([3, abs(int(rightStick[1] * 100)), int(rightStick[1] > 0), 10])

	i2c.sendBlockData(address, mode, data)

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

	actuateTorso()
	actuateHead()

def setMode():
	global mode
	if controller.A():
		mode = MODE_NAVIGATE
	elif controller.B():
		mode = MODE_MANIPULATE

def modeToString():
	global mode
	if mode == MODE_NAVIGATE:
		return "Navigate  "
	elif mode == MODE_MANIPULATE:
		return "Manipulate"
		
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
