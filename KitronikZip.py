# microbit-module: KitronikZip@1.0.0
# Copyright (c) Kitronik Ltd 2019. 
from neopixel import NeoPixel
import math
class ZipLEDs(NeoPixel):
 brPer=50
 allZ=[0]
 lastRng=0
 def __init__(s,pin,numZips):
  for zips in range(1,len(s)): s.allZ.append(0)
 def setColour(s,col,zipRng=0):
  if (zipRng!=0): 
   for z in range(s.allZ.index(zipRng),(s.allZ.index(zipRng)+s.allZ.count(zipRng))): s[z]=col
  else: 
   for z in range(0,len(s)): s[z]=col
  s._applyBrightness()
 def showColour(s,col,zipRng=0):
  s.setColour(col,zipRng)
  s.show()
 def showZip(s,zips,col):
  s.setZipColour(zips,col)
  s.show()
 def setZipColour(s,zips,col):
  s[zips]=col
  s._applyBrightness()
 def rotate(s,rotBy):
  rot=0
  if(rotBy>0):
   while rot<rotBy:
    zips = s[len(s)-1]
    for z in range(len(s)-1,0,-1):
     s[z]=s[z-1]
    s[0]=zips
    rot=rot+1
  else:
   while rot>rotBy:
    zips=s[0]
    for z in range(0,len(s)-1):
     s[z]=s[z+1]
    s[len(s)-1]=zips
    rot=rot-1
 def setBrightness(s,br):
  s.brPer=br
  if (s.brPer<=0): s.brPer=1
  elif (s.brPer>100): s.brPer=100
 def _applyBrightness(s):
  for z in range(0,len(s)):
   r=s[z][0]
   g=s[z][1]
   b=s[z][2]
   brMul=2.55*s.brPer
   if (r==0) and (g==0) and (b==0): rBr,gBr,bBr=0,0,0
   else:
    if (r>g):
     if (r>b):
      rRat=r/r
      gRat=g/r
      bRat=b/r
     else:
      rRat=r/b
      gRat=g/b
      bRat=b/b
    else:
     if (g>b):
      rRat=r/g
      gRat=g/g
      bRat=b/g
     else:
      rRat=r/b
      gRat=g/b
      bRat=b/b
    rBr=math.floor(brMul*rRat)
    gBr=math.floor(brMul*gRat)
    bBr=math.floor(brMul*bRat)
   s[z]=(rBr,gBr,bBr)
 def createRange(s,sZip,l):
  if (sZip>(len(s)-1)): sZip=(len(s)-1)
  if ((sZip+l)>len(s)): l=l-((sZip+l)-len(s))
  setRng=s.lastRng+1
  if (s.allZ[sZip]!=0):
   setRng=s.allZ[sZip]
   for z in range(0,len(s)):
    if (s.allZ[z]==setRng): s.allZ[z]=0
  else: s.lastRng+=1
  for z in range(sZip,(sZip+l)): s.allZ[z]=setRng
 def showRainbow(s,strtHue,endHue,zipRng=0):
  hueRng=math.fabs(endHue-strtHue)
  if (zipRng!=0):
   rngLeds=s.allZ.count(zipRng)
   rngstrt=s.allZ.index(zipRng)
   hueStep=hueRng/rngLeds
  else: hueStep=hueRng/len(s)
  if(strtHue<endHue):
   if (zipRng!=0):
    for z in range(rngstrt,(rngstrt+rngLeds)): s[z]=s.hueToRGB(strtHue+((z-rngstrt)*hueStep))
   else:
    for z in range(0,len(s)): s[z]=s.hueToRGB(strtHue+(z*hueStep))
  else:
   if (zipRng!=0):
    for z in range(rngstrt,(rngstrt+rngLeds)): s[z]=s.hueToRGB(endHue-((z-rngstrt)*hueStep))
   else:
    for z in range(0,len(s)): s[z]=s.hueToRGB(endHue-(z*hueStep))
  s._applyBrightness()
  s.show()
 def zipwavlen(s,wavlen):
   rVal,gVal,bVal=0,0,0
   if ((wavlen>=470) and (wavlen<525)):
    gVal=math.floor((wavlen-470)*4.6364)
    bVal=255-gVal 
   elif ((wavlen>=525) and (wavlen<=625)):
    rVal=math.floor((wavlen-525)*2.55)
    gVal=255-rVal
   return (rVal,gVal,bVal)
 def hueToRGB (s,hue):
  rVal,gVal,bVal=0,0,0
  hueStep=2.125
  if ((hue>=0) and (hue<120)):
   gVal=math.floor(hue*hueStep)
   rVal=255-gVal
  elif ((hue>=120) and (hue<240)):
   bVal=math.floor((hue-120)*hueStep)
   gVal=255-bVal
  elif ((hue>=240) and (hue<360)):
   rVal=math.floor((hue-240)*hueStep)
   bVal=255-rVal
  return (rVal,gVal,bVal)
 def showBarGraph(s,valToDisp,rng): 
  if (rng<=0):
   s.clear()
   s.showZip(0,(0,255,0))
  else:
   value=math.fabs(valToDisp)
   numZips=len(s)
   vis=(value*numZips)//rng
   for i in range(numZips):
    if(i<=vis):
     gVal=(i*255)//(numZips-1)
     s.setZipColour(i,(gVal,255-gVal,0))
    else: s.setZipColour(i,(0,0,0))
  s._applyBrightness()
  s.show()