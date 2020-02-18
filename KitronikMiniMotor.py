# microbit-module: KitronikMiniMotor@1.0.0
# Copyright (c) Kitronik Ltd 2019.
"""
The MIT License (MIT)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

Using the module:
- Setup motors, stepper motors and servos at the start of the program:
 * New Motor: m1 = Motor(pin13,pin14) [Note: Motor pin pairs are pin13 & pin14 or pin15 & pin16]
 * New Stepper Motor: stepper = StepperMotor()
 * New Servo: sv = Servo(pin0) [Note: Servo pins are either pin0 or pin8]

- Controlling motors, stepper motors and servos:
 * Drive Motors: m1.drive("cw",100) [Note: Direction is "cw" or "c_cw", speed 1 to 100)
 * Stop Motors: m1.stop()
 * Drive Stepper Motor (Steps): stepper.turnSteps("cw",50,50) [Note: Direction is "cw" or "c_cw", steps 1 to 200 (default), speed 1 to 100%]
  - Change default stepper steps: settings.stepperMotorSteps = "NEW NUMBER OF STEPS"
 * Drive Stepper Motor (Angle): stepper.turnAngle("c_cw",180,100) [Note: Angle 1 to 360, speed 1 to 100%]
 * Turn Servo: sv.write_angle(90) [Note: Angle 0 to 180]
"""

from microbit import *
import math

class settings:
 stepperMotorSteps = 200
 stepStage = 1

class Motor:
 def __init__(self,pinA,pinB):
  self.pinA = pinA
  self.pinB = pinB

 def drive(self,direction,speed):
  if (speed<0): speed=0
  elif (speed>100): speed=100
  speedOP=math.floor(speed*(1023/100))
  if (direction=="c_cw"):
   self.pinA.write_analog(speedOP)
   self.pinB.write_digital(0)
  elif (direction=="cw"):
   self.pinA.write_digital(0)
   self.pinB.write_analog(speedOP)

 def stop(self):
  self.pinA.write_digital(0)
  self.pinB.write_digital(0)

class StepperMotor:
 def __init__(self,pinA=pin13,pinB=pin14,pinC=pin15,pinD=pin16):
  self.coil1 = Motor(pinA,pinB)
  self.coil2 = Motor(pinC,pinD)

 def turnAngle(self,direction,angle,speed):
  angleToSteps = 0
  angleToSteps = ((angle - 1) * (settings.stepperMotorSteps - 1)) / (360 - 1) + 1
  angleToSteps = int(angleToSteps)
  if speed < 1: speed = 1
  if speed > 100: speed = 100
  speedDelay = math.floor(80 - ((speed/100)*68))
  self._driveMotor(direction,angleToSteps,speedDelay)

 def turnSteps(self,direction,stepperSteps,speed):
  if speed < 1: speed = 1
  if speed > 100: speed = 100
  speedDelay = math.floor(80 - ((speed/100)*68))
  self._driveMotor(direction,stepperSteps,speedDelay)

 def _driveMotor(self,direction,steps,speedDelay):
  stepCounter = 0
  while stepCounter < steps:
   if settings.stepStage == 1 or settings.stepStage == 3:
    currentCoil = 1
   else:
    currentCoil = 2

   if settings.stepStage == 1 or settings.stepStage == 4:
    currentDirection = "c_cw"
   else:
    currentDirection = "cw"

   if currentCoil == 1:
    self.coil1.drive(currentDirection,100)
   elif currentCoil == 2:
    self.coil2.drive(currentDirection,100)
   sleep(speedDelay)

   if direction == "c_cw":
    if settings.stepStage == 4:
     settings.stepStage = 1
    else:
     settings.stepStage += 1
   elif direction == "cw":
    if settings.stepStage == 1:
     settings.stepStage = 4
    else:
     settings.stepStage -= 1

   stepCounter += 1

class Servo:
 def __init__(self,pin,freq=50,min_us=600,max_us=2400,angle=180):
  self.min_us = min_us
  self.max_us = max_us
  self.us = 0
  self.freq = freq
  self.angle = angle
  self.analog_period = 0
  self.pin = pin
  analog_period = round((1/self.freq)*1000)
  self.pin.set_analog_period(analog_period)

 def _write_us(self,us):
  us = min(self.max_us,max(self.min_us,us))
  duty = round(us*1024*self.freq//1000000)
  self.pin.write_analog(duty)

 def write_angle(self,degrees=None):
  degrees = degrees%360
  total_range = self.max_us-self.min_us
  us = self.min_us+total_range*degrees//self.angle
  self._write_us(us)