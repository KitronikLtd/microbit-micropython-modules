# microbit-module: KitronikGameController@1.0.0
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
import music

class buttons:
    Up = pin8
    Down = pin14
    Left = pin12
    Right = pin13
    Fire_1 = pin15
    Fire_2 = pin16

class settings:
    musicPin = pin2        
    
# Determines whether a particular button has been pressed (returns True or False)
def onButtonPress(button):
    if button.read_digital() == 0:
        return True
    else:
        return False

# Buzzer
# Play a single frequency tone on the buzzer for a specified length in ms
def playTone(frequency, toneLength):
    music.pitch(frequency, toneLength, settings.musicPin, True)

# Play a tune from the standard list on the buzzer (once or forever until stopMusic() is called)
def playMelody(tune, repeat):
    music.play(tune, settings.musicPin, False, repeat)

# Stop all music from the buzzer
def stopMusic():
    music.stop(settings.musicPin)

# Run Motor for length of time specified in ms
def runMotor(length):
    pin1.write_digital(1)
    sleep(length)
    pin1.write_digital(0)