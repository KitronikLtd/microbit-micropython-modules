# microbit-module: KitronikPiano@1.0.0
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
from microbit import *
from micropython import const

class PianoKeys:
 KEY_K0=0x100
 KEY_K1=0x200
 KEY_K2=0x400
 KEY_K3=0x800
 KEY_K4=0x1000
 KEY_K5=0x2000
 KEY_K6=0x4000
 KEY_K7=0x8000
 KEY_K8=0x01
 KEY_K9=0x02
 KEY_K10=0x04
 KEY_K11=0x08
 KEY_K12=0x10
 KEY_K13=0x20
 KEY_K14=0x40

#Class for driving the Kitronik :KLEF Piano
class Piano:
 _CHIP_ADDR=const(0x0D)
 keyRegValue=0x0000
 buff=bytearray(1)
 buff2=bytearray(2)
 buff3=bytearray(5)

 #Function to initialise the micro:bit Piano (called automatically on instantiation)
 def __init__(s,sense=8,noise=5):
  pin1.set_pull(pin1.PULL_UP)
  # Startup procedure
  # Test /change pin is low, then test basic communication
  if (pin1.read_digital()==0):
   # Reads the chip ID, should be 0x11 (chip ID addr = 0)
   s.buff[0] = 0
   i2c.write(s._CHIP_ADDR, s.buff, False)
   s.buff = i2c.read(s._CHIP_ADDR, 1, False)
   while s.buff[0] != 0x11:
    s.buff = i2c.read(s._CHIP_ADDR, 1, False)
   # Change sensitivity (burst length) of keys 0-14 to 'sense' (default is 8)
   for sensitivityReg in range(54, 69, 1):
    s.buff2[0] = sensitivityReg
    s.buff2[1] = sense
    i2c.write(s._CHIP_ADDR, s.buff2, False)
   # Disable key 15 as it is not used
   s.buff2[0] = 69
   s.buff2[1] = 0
   i2c.write(s._CHIP_ADDR, s.buff2, False)
   # Set Burst Repetition to 'noise' (default is 5)
   s.buff2[0] = 13
   s.buff2[1] = noise
   i2c.write(s._CHIP_ADDR, s.buff2, False)
   #Configure Adjacent Key Suppression (AKS) Groups
   #AKS Group 1: ALL KEYS
   for aksReg in range(22, 37, 1):
    s.buff2[0] = aksReg
    s.buff2[1] = 1
    i2c.write(s._CHIP_ADDR, s.buff2, False)
   # Send calibration command
   s.buff2[0] = 10
   s.buff2[1] = 1
   i2c.write(s._CHIP_ADDR, s.buff2, False)
  # Read all change status address (General Status addr = 2)
  s.buff[0] = 2
  i2c.write(s._CHIP_ADDR, s.buff, False)
  s.buff3 = i2c.read(s._CHIP_ADDR, 5, False)
  # Continue reading change status address until /change pin goes high
  while (pin1.read_digital()==0):
   s.buff[0] = 2
   i2c.write(s._CHIP_ADDR, s.buff, False)
   s.buff3 = i2c.read(s._CHIP_ADDR, 5, False)

 #Set sensitivity & noise threshold of capacitive touch keys, then initialise the IC.
 #Sensitivity: A higher value increases the sensitivity (values can be in the range 1 - 32).
 #Noise Threshold: A higher value enables the piano to be used in areas with more electrical noise (values can be in the range 1 - 63).
 def changeSettings(s,sensitivity,noiseThreshold):
  s.__init__(sensitivity,noiseThreshold)

 #Function to read the Key Press Registers
 #Return value is a combination of both registers (3 and 4) which links with the values in the 'PianoKeys' class
 def _readKeyPress(s):
  s.buff[0] = 2
  i2c.write(s._CHIP_ADDR, s.buff, False)
  s.buff3 = i2c.read(s._CHIP_ADDR, 5, False)
  # Address 3 is the addr for keys 0-7 (this will then auto move onto Address 4 for keys 8-15, both reads stored in buff2)
  s.buff[0] = 3
  i2c.write(s._CHIP_ADDR, s.buff, False)
  s.buff2 = i2c.read(s._CHIP_ADDR, 2, False)
  # keyRegValue is a 4 byte number which shows which keys are pressed
  keyRegValue = (s.buff2[1] + (s.buff2[0]*256))
  return keyRegValue

 #Function to determine if a piano key is pressed and returns a true or false output.
 def keyIsPressed(s, key: PianoKeys):
  keyPressed = False
  if (key & s._readKeyPress()) == key:
      keyPressed = True
  return keyPressed