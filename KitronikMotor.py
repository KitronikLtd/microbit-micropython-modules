# microbit-module: KitronikMotor@1.0.0
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
import math

class MotorDriver:
 def __init__(s,m1pinA,m1pinB,m2pinA,m2pinB):
  s.motor1PinA=m1pinA
  s.motor1PinB=m1pinB
  s.motor2PinA=m2pinA
  s.motor2PinB=m2pinB

 def motorOn(s,motor,direct,speed):
  if (speed<0): speed=0
  elif (speed>100): speed=100
  speedOP=math.floor(speed*(1023/100))
  if (motor==1):
   if (direct=="forward"):
    s.motor1PinA.write_analog(speedOP)
    s.motor1PinB.write_digital(0)
   elif (direct=="reverse"):
    s.motor1PinA.write_digital(0)
    s.motor1PinB.write_analog(speedOP)
  elif (motor==2):
   if (direct=="forward"):
    s.motor2PinA.write_analog(speedOP)
    s.motor2PinB.write_digital(0)
   elif (direct=="reverse"):
    s.motor2PinA.write_digital(0)
    s.motor2PinB.write_analog(speedOP)

 def motorOff(s,motor):
  if (motor==1):
   s.motor1PinA.write_digital(0)
   s.motor1PinB.write_digital(0)
  elif (motor==2):
   s.motor2PinA.write_digital(0)
   s.motor2PinB.write_digital(0)