# microbit-module: kitronikClipDetector@0.0.1
from microbit import pin0
from microbit import pin1
from microbit import pin2

class Detector:
    global sensorLeftRef
    global sensorCentreRef
    global sensorRightRef
    global detectionLevel

    def __init__(self):
        self.sensorLeftRef = pin0.read_analog()
        self.sensorCentreRef = pin1.read_analog()
        self.sensorRightRef = pin2.read_analog()
        self.detectionLevel = 45

    def sensorSetup(self, DetectionSelection):
        #reading is done by converted ADC reading for a voltage change of the sensor
        if DetectionSelection is "Line":
            self.detectionLevel = 45
        elif DetectionSelection is "Light":
            self.detectionLevel = 55
        elif DetectionSelection is "Object":
            self.detectionLevel = 16

    def readAnalogSensor(self, pin):
        if pin == "P0":
            value = pin0.read_analog()
        elif pin == "P1":
            value = pin1.read_analog()
        elif pin == "P2":
            value = pin2.read_analog()
        return value

    def readDigitalSensor(self, pin, lightLevel):
        if pin == "P0":
            value = pin0.read_analog()
            ref = self.sensorLeftRef
        elif pin == "P1":
            value = pin1.read_analog()
            ref = self.sensorCentreRef
        elif pin == "P2":
            value = pin2.read_analog()
            ref = self.sensorRightRef

        if lightLevel == "Light":
            if (value >= (ref + self.detectionLevel)):
                result = True
            else:
                result = False
        elif lightLevel == "Dark":
            if (value <= (ref - self.detectionLevel)):
                result = True
            else:
                result = False
        return result