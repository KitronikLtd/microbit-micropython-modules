# microbit-module: KitronikZip@1.0.0
# A module for the Kitronik Zip LEDs

from neopixel import NeoPixel
import math

class ZipColours:

		Red = (255,0,0)
		Orange = (255,165,0)
		Yellow = (255,255,0)
		Green = (0,255,0)
		Blue = (0,0,255)
		Indigo = (75,0,130)
		Violet = (138,43,226)
		Purple = (255,0,255)
		White = (255,255,255)
		Black = (0,0,0)


class ZipLEDs(NeoPixel):
    brightnessValue = 128
    #Set all thepixels to a colour
    def setColour(self,colourToSet):
        for pixel_id in range(0,len(self)):
            self[pixel_id] = colourToSet

    #Show the colour on all the ZipLeds
    def showColour(self,colourToShow):
        self.setColour(colourToShow)
        self.show()

    #Set a pixel to a colour but dont show it
    def setPixelColour(self,pixel,colourToSet):
        self[pixel] = colourToSet

    #suboptimal code because NeoPixel not really a list, it just has list like tendencies
    def rotate(self, rotateBy):
        rotated = 0
        if(rotateBy > 0): #shift up
            while rotated < rotateBy:
                pixel = self[len(self)-1]
                for pixel_id in range(len(self)-1,0,-1):
                    self[pixel_id] = self[pixel_id-1]
                self[0] = pixel
                rotated = rotated+1
        else: #shift down
            while rotated > rotateBy:
                pixel = self[0]
                for pixel_id in range(0,len(self)-1):
                    self[pixel_id] = self[pixel_id+1]
                self[len(self)-1] = pixel
                rotated = rotated-1 #avoid an ABS calculation for all the saving that it gives...
    
    
    
    #TODO actually implement some brightness stuff. 
    #Would be better in the assembler code as per the Kitronik implementation for makecode
    def setBrightness(self,brightness):
        brightnessValue = brightness
    
    #def range(self, fromPixel, howMany):
    
    
    #def showBarGraph(self,valueToDisplay, Max):
      
        
    def zipWavelength(self, wavelength):
        blueGreen = 4.6364
        redGreen = 2.55
        redVal = 0
        greenVal = 0
        blueVal = 0
       #The LEDs we are using have centre wavelengths of 470nm(Blue) 525nm(Green) and 625nm (Red) 
       #We blend these linearly to give the impression of the other wavelengths. 
        if ((wavelength >= 470) and (wavelength < 525)):
            #We are between Blue and Green so mix those
            greenVal = math.floor((wavelength - 470) * blueGreen)
            blueVal = 255 - greenVal 
        elif ((wavelength >= 525) and (wavelength <= 625)):
            #we are between Green and Red, so mix those
            redVal = math.floor((wavelength - 525) * redGreen)
            greenVal = 255 - redVal
        return (redVal, greenVal, blueVal)

    def hueToRGB (self, hue): #probably will optimaise this away later.
        redVal =0
        greenVal =0
        blueVal =0            
        hueStep = 2.125 
        if ((hue >= 0) and (hue < 120)): #RedGreen section
            #We are between Blue and Green so mix those
            greenVal = math.floor((hue) * hueStep)
            redVal = 255 - greenVal 
        elif ((hue >= 120) and (hue < 240)): #GreenBlueSection
            #we are between Green and Red, so mix those
            blueVal = math.floor((hue-120) * hueStep)
            greenVal = 255 - blueVal
        elif ((hue >= 240) and (hue < 360)): #GreenBlueSection
            #we are between Green and Red, so mix those
            redVal = math.floor((hue-240) * hueStep)
            blueVal = 255 - redVal

        return (redVal, greenVal, blueVal)

            
    def showRainbow(self,startHue,endHue):
        hueRange = math.fabs(endHue-startHue)
        hueStep = hueRange/len(self)
        if(startHue<endHue): #conventional rainbow
            for pixel_id in range(0,len(self)):
                self[pixel_id] = self.hueToRGB(startHue+(pixel_id * hueStep))
        else:#draw the rainbow backwards
            for pixel_id in range(0,len(self)):
                self[pixel_id] = self.hueToRGB(endHue-(pixel_id * hueStep))
        self.show()