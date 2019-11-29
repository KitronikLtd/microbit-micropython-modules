# microbit-module: kitronikInterfaceForFischertechnik@0.0.1
from microbit import *
import math

class Interface:
    
    def motorOn(self, motor, direction, speed):
        
        if speed > 100:
            speed = 100
        elif speed < 0:
            speed = 0
        speed = speed * 10
        if motor == "Motor1":
            if direction == "forward":
                pin8.write_analog(speed)
                pin12.write_digital(0)
            elif direction == "reverse":
                pin12.write_analog(speed)
                pin8.write_digital(0)
        elif motor == "Motor2":
            if direction == "forward":
                pin16.write_analog(speed)
                pin2.write_digital(0)
            elif direction == "reverse":
                pin2.write_analog(speed)
                pin16.write_digital(0)

    def motorOff(self, motor):
        if motor == "Motor1":
            pin12.write_digital(0)
            pin8.write_digital(0)
        elif motor == "Motor2":
            pin2.write_digital(0)
            pin16.write_digital(0)
    
    def led(self, pinSelection, illumination):
        if pinSelection == "P0":
            if illumination == "on":
                pin0.write_digital(1)
            elif illumination == "off":
                pin0.write_digital(0)
        elif pinSelection == "P1":
            if illumination == "on":
                pin1.write_digital(1)
            elif illumination == "off":
                pin1.write_digital(0)
    
    def phototransistor(self, pinSelection):
        if pinSelection == "P0":
            reading = pin0.read_analog()
        elif pinSelection == "P1":
            reading = pin1.read_analog()
        return reading
            
    def ntc(self, pinSelection):
        if pinSelection == "P0":
            reading = pin0.read_analog()
        elif pinSelection == "P1":
            reading = pin1.read_analog()
        convertReading = reading * (3.3/1024)       # convert reading to voltage reading x (supply divide ADC resoluction)
        ntcResistor = 3.3/((3.3-convertReading)/4700)  # calculate resistance
        temperatureC = (3880/math.log(ntcResistor/0.13)) - 273.15
        return temperatureC