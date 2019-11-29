# microbit-module: kitronikStopbit@0.0.1
from microbit import pin0
from microbit import pin1
from microbit import pin2
# Kitronik STOP:bit blocks

class Stopbit:
	# turn each LED on or off individually
	def Light(colour, illuminate):    
		if colour == "Red": 
			if illuminate == "On":
				pin0.write_digital(1)
			elif illuminate == "Off":
				pin0.write_digital(0)
		elif colour == "Yellow":
			if illuminate == "On":
				pin1.write_digital(1)
			elif illuminate == "Off":
				pin1.write_digital(0)  
		elif colour == "Green":
			if illuminate == "On":
				pin2.write_digital(1)
			elif illuminate == "Off":
				pin2.write_digital(0)     

	# turn each LED on or off individually
	def State(state): 
		if state == "stop":
			pin0.write_digital(1)
			pin1.write_digital(0)
			pin2.write_digital(0)
		elif state == "getReady":
			pin0.write_digital(1)
			pin1.write_digital(1)
			pin2.write_digital(0) 
		elif state == "go":
			pin0.write_digital(0)
			pin1.write_digital(0)
			pin2.write_digital(1)    
		elif state == "readyToStop":
			pin0.write_digital(0)
			pin1.write_digital(1)
			pin2.write_digital(0)    
