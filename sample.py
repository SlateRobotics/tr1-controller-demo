import sys
import i2c_wrapper
import xbox_controller
import helper
import numpy as np
from time import sleep

sys.stdout.write("Program starting up...")

ADDRESS_BASE_MOTORS = 0x70
ADDRESS_TORSO_ACTUATOR = 0x71

MODE_NAVIGATE = 0
MODE_MANIPULATE = 1

i2c = i2c_wrapper.i2c()
controller = xbox_controller.getController()
mode = MODE_NAVIGATE

def navigate():
	address = ADDRESS_BASE_MOTORS
	mode = 0

	leftStick = controller.leftStick()
	motorValues = helper.getMotorValues(np.array(leftStick))
	data = [1, int(abs(motorValues[0]) * 100), int(motorValues[0] < 0), 10]
	data.extend([2, int(abs(motorValues[1]) * 100), int(motorValues[1] < 0), 10])
	data.extend([3, int(abs(motorValues[2]) * 100), int(motorValues[2] < 0), 10])
	data.extend([4, int(abs(motorValues[3]) * 100), int(motorValues[3] < 0), 10])

	i2c.sendBlockData(address, mode, data)

def manipulate():
	address = 0x00
	mode = 0
	data = []
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

def controlRobot():
	global mode
	if mode == MODE_NAVIGATE:
		navigate()
	elif mode == MODE_MANIPULATE:
		manipulate()

	actuateTorso()

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
		sys.stdout.write("\rController disconnected")

	sleep(0.050)
	sys.stdout.flush()

sys.stdout.write("\nBack button pressed. Exiting...\n")
controller.close()
