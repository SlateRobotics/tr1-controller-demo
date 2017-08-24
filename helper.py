import sys
import numpy as np
import math

# input: numpy array
def getMotorValues(desiredVector):
	if desiredVector.size == 0:
		return (0, 0, 0, 0)

	desiredX = desiredVector.tolist()[0]
	desiredY = desiredVector.tolist()[1]
	desiredMagnitude = abs(desiredX)
	if abs(desiredY) > desiredMagnitude:
		desiredMagnitude = abs(desiredY)

	if desiredMagnitude == 0:
		return (0, 0, 0, 0)

	# create rotation matrix
	offset = math.pi / 4
	c, s = np.cos(offset), np.sin(offset)
	rotationMatrix = np.matrix('{} {}; {} {}'.format(c, -s, s, c))

	# create motorVector from rotation matrix and desiredVector
	ouput = desiredVector.dot(rotationMatrix).tolist()[0]

	# scale output to match desired magnitude
	outputX = ouput[0]
	outputY = ouput[1]
	outputMagnitude = abs(outputX)
	if abs(outputY) > outputMagnitude:
		outputMagnitude = abs(outputY)

	scale = desiredMagnitude / outputMagnitude
	scaledOutput = (outputX * scale, outputY * scale)

	return (scaledOutput[1], scaledOutput[0], scaledOutput[1], scaledOutput[0])

