# microbit-module: kitronikGameController@0.0.1
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