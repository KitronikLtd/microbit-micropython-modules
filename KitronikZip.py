# microbit-module: KitronikZip@1.0.0
from neopixel import NeoPixel
import math

class ZipColours:
#Class to hold human readable colours
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
 brightPer = 50 #Default is 50%
 #len(self)
 #Set all Zip LEDs to a colour
 def setColour(self,colourToSet,start=0,length=60):
  for pixel_id in range(start,start+length):
   self[pixel_id] = colourToSet
  self._applyBrightness()

 #Show the colour on all the Zip LEDs
 def showColour(self,colourToShow):
  self.setColour(colourToShow)
  self._applyBrightness()
  self.show()

 #Show colour on a single Zip LED 
 def showPixel(self,pixel,colourToShow):
  self.setPixelColour(pixel,colourToShow)
  self._applyBrightness()
  self.show()

 #Set a Zip LED to a colour
 def setPixelColour(self,pixel,colourToSet):
  self[pixel] = colourToSet
  self._applyBrightness()

 #Suboptimal as NeoPixel not really a list (list like tendencies)
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

 #Set brightness percentage, changes brightPer
 #0 not allowed, causes zero divide error
 def setBrightness(self, brightness):
  self.brightPer = brightness
  if (self.brightPer <= 0):
   self.brightPer = 1
  elif (self.brightPer > 100):
   self.brightPer = 100

 #Apply the brightness setting
 def _applyBrightness(self):
  for pixel_id in range(0,len(self)):
   r = self[pixel_id][0]
   g = self[pixel_id][1]
   b = self[pixel_id][2]
   brMul = 2.55*self.brightPer #brMul = (255/100)*brightPer
   if (r == 0) and (g == 0) and (b ==0):
    rBr, gBr, bBr = 0, 0, 0
   elif (r > g): # r > g
    if (r > b): # r > b
     rRatio = r/r
     gRatio = g/r
     bRatio = b/r
    else: # b > r
     rRatio = r/b
     gRatio = g/b
     bRatio = b/b
   else: # g > r
    if (g > b):
     rRatio = r/g
     gRatio = g/g
     bRatio = b/g
    else: # b > g
     rRatio = r/b
     gRatio = g/b
     bRatio = b/b
   rBr = math.floor(brMul*rRatio)
   gBr = math.floor(brMul*gRatio)
   bBr = math.floor(brMul*bRatio)
   self[pixel_id] = (rBr, gBr, bBr)

 def zipWavelength(self, wavelength):
  blueGreen = 4.6364
  redGreen = 2.55
  redVal = 0
  greenVal = 0
  blueVal = 0
 #Zip LEDs have centre wavelengths of 470nm(Blue), 525nm(Green) & 625nm(Red) 
 #Blended linearly to give impression of other wavelengths 
  if ((wavelength >= 470) and (wavelength < 525)):
   #Between Blue and Green so mix those
   greenVal = math.floor((wavelength - 470) * blueGreen)
   blueVal = 255 - greenVal 
  elif ((wavelength >= 525) and (wavelength <= 625)):
   #Between Green and Red so mix those
   redVal = math.floor((wavelength - 525) * redGreen)
   greenVal = 255 - redVal
  return (redVal, greenVal, blueVal)

 def hueToRGB (self, hue):
  redVal =0
  greenVal =0
  blueVal =0
  hueStep = 2.125
  if ((hue >= 0) and (hue < 120)): #RedGreen section
   greenVal = math.floor((hue) * hueStep)
   redVal = 255 - greenVal
  elif ((hue >= 120) and (hue < 240)): #GreenBlueSection
   blueVal = math.floor((hue-120) * hueStep)
   greenVal = 255 - blueVal
  elif ((hue >= 240) and (hue < 360)): #BlueRedSection
   redVal = math.floor((hue-240) * hueStep)
   blueVal = 255 - redVal

  return (redVal, greenVal, blueVal)

 def showRainbow(self,startHue,endHue):
  hueRange = math.fabs(endHue-startHue)
  hueStep = hueRange/len(self)
  if(startHue<endHue): #conventional rainbow
   for pixel_id in range(0,len(self)):
    self[pixel_id] = self.hueToRGB(startHue+(pixel_id * hueStep))
  else:#draw rainbow backwards
   for pixel_id in range(0,len(self)):
    self[pixel_id] = self.hueToRGB(endHue-(pixel_id * hueStep))
  self._applyBrightness()
  self.show()

 #Bar graph of green(lowest value) to red (Range)
 def showBarGraph(self, valueToDisplay, graphRange): 
  if (graphRange <= 0): #-ve value doesnt make sense, so just turn on first LED as green
   self.clear()
   self.showPixel(0,ZipColours.Green)
  else:
   value = math.fabs(valueToDisplay) #only interested in magnitude
   numberOfPixels = len(self)
   visible = (value * numberOfPixels)//graphRange
   for i in range(numberOfPixels):
    if(i <= visible):
     greenVal =(i * 255)//(numberOfPixels-1)
     self.setPixelColour(i, (greenVal, 255 - greenVal, 0))
    else:
     self.setPixelColour(i, (0,0,0)) #turn off pixels over the display value
  self._applyBrightness()
  self.show()

class RangeLEDs():
 def __init__(self, startPixel, length):
  self.start = startPixel
  self.len = length

 def setColour(self,zipLeds,colourToSet):
  zipLeds.setColour(colourToSet,self.start,self.len)