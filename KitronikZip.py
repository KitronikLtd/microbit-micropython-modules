# microbit-module: KitronikZip@1.0.0
from neopixel import NeoPixel
import math

class ZipLEDs(NeoPixel):
 brightPer=50 #Default 50%
 zipLeds=[0]
 lastRange=0

 def __init__(self,pin,numZips):
  for pixels in range(1,len(self)):
   self.zipLeds.append(0)

 #Set all Zip LEDs to a colour
 def setColour(self,colToSet,zipRange=0):
  if (zipRange!=0):
   for zip_id in range(self.zipLeds.index(zipRange),(self.zipLeds.index(zipRange)+self.zipLeds.count(zipRange))):
    self[zip_id]=colToSet
  else:
   for zip_id in range(0,len(self)):
    self[zip_id]=colToSet
  self._applyBrightness()

 #Show the colour on all the Zip LEDs
 def showColour(self,colToShow,zipRange=0):
  self.setColour(colToShow,zipRange)
  self.show()

 #Show colour on a single Zip LED 
 def showZip(self,zips,colToShow):
  self.setZipColour(zips,colToShow)
  self.show()

 #Set a Zip LED to a colour
 def setZipColour(self,zips,colToSet):
  self[zips]=colToSet
  self._applyBrightness()

 #Suboptimal as NeoPixel not really a list (list like tendencies)
 def rotate(self,rotBy):
  rot=0
  if(rotBy>0): #shift up
   while rot<rotBy:
    zips = self[len(self)-1]
    for zip_id in range(len(self)-1,0,-1):
     self[zip_id]=self[zip_id-1]
    self[0]=zips
    rot=rot+1
  else: #shift down
   while rot>rotBy:
    zips=self[0]
    for zip_id in range(0,len(self)-1):
     self[zip_id]=self[zip_id+1]
    self[len(self)-1]=zips
    rot=rot-1 #avoid an ABS calculation for all the saving that it gives...

 #Set brightness percentage, changes brightPer
 #0 not allowed, causes zero divide error
 def setBrightness(self,bright):
  self.brightPer=bright
  if (self.brightPer<=0):
   self.brightPer=1
  elif (self.brightPer>100):
   self.brightPer=100

 #Apply the brightness setting
 def _applyBrightness(self):
  for zip_id in range(0,len(self)):
   r=self[zip_id][0]
   g=self[zip_id][1]
   b=self[zip_id][2]
   brMul=2.55*self.brightPer #brMul=(255/100)*brightPer
   if (r==0) and (g==0) and (b==0):
    rBr,gBr,bBr=0,0,0
   else:
    if (r>g): #r>g
     if (r>b): #r>b
      rRatio=r/r
      gRatio=g/r
      bRatio=b/r
     else: #b>r
      rRatio=r/b
      gRatio=g/b
      bRatio=b/b
    else: #g>r
     if (g>b):
      rRatio=r/g
      gRatio=g/g
      bRatio=b/g
     else: #b>g
      rRatio=r/b
      gRatio=g/b
      bRatio=b/b
    rBr=math.floor(brMul*rRatio)
    gBr=math.floor(brMul*gRatio)
    bBr=math.floor(brMul*bRatio)
   self[zip_id]=(rBr,gBr,bBr)

 def createRange(self,startZip,length):
  if (startZip>(len(self)-1)):
   startZip=(len(self)-1)
  if ((startZip+length)>len(self)):
   length=length-((startZip+length)-len(self))
  setRange=self.lastRange+1
  if (self.zipLeds[startZip]!=0):
   setRange=self.zipLeds[startZip]
   for zips in range(0,len(self)):
    if (self.zipLeds[zips]==setRange):
     self.zipLeds[zips]=0
  else:
   self.lastRange+=1 #only if adding new range
  for zip_id in range(startZip,(startZip+length)):
   self.zipLeds[zip_id]=setRange

 def showRainbow(self,startHue,endHue,zipRange=0):
  hueRange=math.fabs(endHue-startHue)
  if (zipRange!=0):
   rangeLeds=self.zipLeds.count(zipRange)
   rangeStart=self.zipLeds.index(zipRange)
   hueStep=hueRange/rangeLeds
  else:
   hueStep=hueRange/len(self)
  if(startHue<endHue): #conventional rainbow
   if (zipRange!=0):
    for zip_id in range(rangeStart,(rangeStart+rangeLeds)):
     self[zip_id]=self.hueToRGB(startHue+((zip_id-rangeStart)*hueStep))
   else:
    for zip_id in range(0,len(self)):
     self[zip_id]=self.hueToRGB(startHue+(zip_id*hueStep))
  else:#draw rainbow backwards
   if (zipRange!=0):
    for zip_id in range(rangeStart,(rangeStart+rangeLeds)):
     self[zip_id]=self.hueToRGB(endHue-((zip_id-rangeStart)*hueStep))
   else:
    for zip_id in range(0,len(self)):
     self[zip_id]=self.hueToRGB(endHue-(zip_id*hueStep))
  self._applyBrightness()
  self.show()

 def zipWavelength(self,wavelength):
   blueGreen=4.6364
   redGreen=2.55
   rVal,gVal,bVal=0,0,0
  #Zip LEDs have centre wavelengths of 470nm(Blue), 525nm(Green) & 625nm(Red) 
  #Blended linearly to give impression of other wavelengths 
   if ((wavelength>=470) and (wavelength<525)):
    #Between Blue and Green so mix those
    gVal=math.floor((wavelength-470)*blueGreen)
    bVal=255-gVal 
   elif ((wavelength>=525) and (wavelength<=625)):
    #Between Green and Red so mix those
    rVal=math.floor((wavelength-525)*redGreen)
    gVal=255-rVal
   return (rVal,gVal,bVal)

 def hueToRGB (self,hue):
  rVal,gVal,bVal=0,0,0
  hueStep=2.125
  if ((hue>=0) and (hue<120)): #RedGreen section
   gVal=math.floor(hue*hueStep)
   rVal=255-gVal
  elif ((hue>=120) and (hue<240)): #GreenBlueSection
   bVal=math.floor((hue-120)*hueStep)
   gVal=255-bVal
  elif ((hue>=240) and (hue<360)): #BlueRedSection
   rVal=math.floor((hue-240)*hueStep)
   bVal=255-rVal
  return (rVal,gVal,bVal)

 #Bar graph of green(lowest value) to red (Range)
 def showBarGraph(self,valueToDisplay,graphRange): 
  if (graphRange<=0): #-ve value doesnt make sense, so just turn on first LED as green
   self.clear()
   self.showZip(0,ZipColours.Green)
  else:
   value=math.fabs(valueToDisplay) #only interested in magnitude
   numberOfZips=len(self)
   visible=(value*numberOfZips)//graphRange
   for i in range(numberOfZips):
    if(i<=visible):
     gVal=(i*255)//(numberOfZips-1)
     self.setZipColour(i,(gVal,255-gVal,0))
    else:
     self.setZipColour(i,(0,0,0)) #turn off pixels over the display value
  self._applyBrightness()
  self.show()