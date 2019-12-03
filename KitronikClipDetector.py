# microbit-module: kitronikClipDetector@1.0.0
# A module for the Kitronik Clip Detector board
# Copyright (c) Kitronik Ltd 2019. 
#
# The MIT License (MIT)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
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