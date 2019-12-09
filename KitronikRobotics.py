# microbit-module: KitronikRobotics@1.0.0
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

class settings:
    PRESCALE_REG = 0xFE
    MODE_1_REG = 0x00
    SRV_REG_BASE = 0x08
    MOT_REG_BASE = 0x28
    REG_OFFSET = 4
    SERVO_MULTIPLIER = 226
    SERVO_ZERO_OFFSET = 0x66

    chipAddress = 0x6C
    initialised = False
    stepStage = 1
    stepper1Steps = 200
    stepper2Steps = 200

def __init():
        
    buf = bytearray(2)

    buf[0] = settings.PRESCALE_REG
    buf[1] = 0x85 #50Hz
    i2c.write(settings.chipAddress, buf, False)
    
    for blockReg in range(0xFA, 0xFE, 1):
        buf[0] = blockReg
        buf[1] = 0x00
        i2c.write(settings.chipAddress, buf, False)

    buf[0] = settings.MODE_1_REG
    buf[1] = 0x01
    i2c.write(settings.chipAddress, buf, False)
    settings.initialised = True

def servoWrite(servo, degrees):
    if settings.initialised is False:
        __init()
    buf = bytearray(2)
    calcServo = settings.SRV_REG_BASE + ((servo - 1) * settings.REG_OFFSET)
    HighByte = False
    PWMVal = (degrees * 100 * settings.SERVO_MULTIPLIER) / (10000 + settings.SERVO_ZERO_OFFSET)
    
    if (PWMVal > 0xFF):
        HighByte = True
    buf[0] = calcServo
    buf[1] = int(PWMVal)
    i2c.write(settings.chipAddress, buf, False)
    buf[0] = calcServo + 1
    if (HighByte):
        buf[1] = 0x01
    else:
        buf[1] = 0x00
    i2c.write(settings.chipAddress, buf, False)

def motorOn(motor, direction, speed):
    if settings.initialised is False:
        __init()
    buf = bytearray(2)
    motorReg = settings.MOT_REG_BASE + (2 * (motor - 1) * settings.REG_OFFSET)
    HighByte = False
    OutputVal = speed * 40
    
    if direction == "forward":
        if OutputVal > 0xFF:
            HighByte = True
            HighOutputVal = int(OutputVal/256)
        buf[0] = motorReg
        buf[1] = int(OutputVal)
        i2c.write(settings.chipAddress, buf, False)
        buf[0] = motorReg + 1
        if HighByte:
            buf[1] = HighOutputVal
        else:
            buf[1] = 0x00
        i2c.write(settings.chipAddress, buf, False)
        
        for offset in range(4, 6, 1):
            buf[0] = motorReg + offset
            buf[1] = 0x00
            i2c.write(settings.chipAddress, buf, False)
        
    elif direction == "reverse":
        if OutputVal > 0xFF:
            HighByte = True
            HighOutputVal = int(OutputVal/256)
        buf[0] = motorReg + 4
        buf[1] = int(OutputVal)
        i2c.write(settings.chipAddress, buf, False)
        buf[0] = motorReg + 5
        if HighByte:
            buf[1] = HighOutputVal
        else:
            buf[1] = 0x00
        i2c.write(settings.chipAddress, buf, False)
        
        for offset2 in range(0, 2, 1):
            buf[0] = motorReg + offset2
            buf[1] = 0x00
            i2c.write(settings.chipAddress, buf, False)

def motorOff(motor):
    buf = bytearray(2)
    motorReg = settings.MOT_REG_BASE + (2 * (motor - 1) * settings.REG_OFFSET)
    
    for offset3 in range(0, 2, 1):
        buf[0] = motorReg + offset3
        buf[1] = 0x00
        i2c.write(settings.chipAddress, buf, False)
    
    for offset4 in range(4, 6, 1):
        buf[0] = motorReg + offset4
        buf[1] = 0x00
        i2c.write(settings.chipAddress, buf, False)

def allOff():
    buf = bytearray(2)
    servoOffCount = 0
    servoRegCount = 0
    
    for motors in range(1, 5, 1):
        motorOff(motors)

    while servoOffCount < 8:
        for offset5 in range(0, 2, 1):
            buf[0] = settings.SRV_REG_BASE + servoRegCount + offset5
            buf[1] = 0x00
            i2c.write(settings.chipAddress, buf, False)

        servoRegCount += 4
        servoOffCount += 1

def stepperMotorTurnAngle(stepper, direction, angle):
    angleToSteps = 0

    if settings.initialised is False: 
        __init()

    if stepper == "Stepper1":
        angleToSteps = ((angle - 1) * (settings.stepper1Steps - 1)) / (360 - 1) + 1
    else:
        angleToSteps = ((angle - 1) * (settings.stepper2Steps - 1)) / (360 - 1) + 1

    angleToSteps = int(angleToSteps)
    _turnStepperMotor(stepper, direction, angleToSteps)

def stepperMotorTurnSteps(stepper, direction, stepperSteps):
    if settings.initialised is False: 
        __init()

    _turnStepperMotor(stepper, direction, stepperSteps)

def _turnStepperMotor(stepper, direction, steps):
    stepCounter = 0

    while stepCounter < steps:
        if settings.stepStage == 1 or settings.stepStage == 3:
            if stepper == "Stepper1":
                currentMotor = 1
            else:
                currentMotor = 3
        else:
            if stepper == "Stepper1":
                currentMotor = 2
            else:
                currentMotor = 4

        if settings.stepStage == 1 or settings.stepStage == 4:
             currentDirection = "forward"
        else:
            currentDirection = "reverse"

        motorOn(currentMotor, currentDirection, 100)
        sleep(20)

        if direction == "forward":
            if settings.stepStage == 4: 
                settings.stepStage = 1
            else:
                settings.stepStage += 1
        elif direction == "reverse":
            if settings.stepStage == 1: 
                settings.stepStage = 4
            else:
                settings.stepStage -= 1
        
        stepCounter += 1
