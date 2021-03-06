import sys
import smbus

class i2c:
	def __init__(self, bus_id = 1):
		self._bus = smbus.SMBus(bus_id)

	def sendBlockData(self, address, mode, data):
		try:
			if address != 0x00 and len(data) != 0:
				self._bus.write_i2c_block_data(address, mode, data)
		except:
			sys.stdout.write("\ni2c error occurred. Continuing...\n")
