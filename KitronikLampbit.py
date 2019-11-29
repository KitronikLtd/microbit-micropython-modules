# microbit-module: kitronikLampbit@0.0.1
from microbit import pin0
from microbit import pin1
# Kitronik LAMP:bit blocks

class Lampbit:
	# turn each LED on or off individually
	def led(illuminate):
		if illuminate == "On":
			pin0.write_digital(1)
		elif illuminate == "Off":
			pin0.write_digital(0)

	# turn each LED on or off individually
	def lightDetect():
		return pin1.read_analog()
