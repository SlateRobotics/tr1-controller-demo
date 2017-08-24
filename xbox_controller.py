import sys
import xbox
from time import sleep

def getController(i=0):
	try:
		return xbox.Joystick()
	except:
		i = i + 1
		sys.stdout.write("\nError setting up to controller. Retrying... (Retry #" + str(i) +")\n")
		sleep(0.2)
		return getController(i + 1);

