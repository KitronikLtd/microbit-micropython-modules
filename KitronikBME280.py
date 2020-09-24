# microbit-module: KitronikBME280@1.0.0
# Copyright (c) Kitronik Ltd 2020. 
from microbit import i2c, pin19, pin20
from micropython import const

class BME280:
 global tempRead
 global presRead
 global humidRead
 global adcRawTemp
 global adcRawPres
 global adcRawHumid

 def i2cRead(s, reg, byte):
  wBuf = bytearray(1)
  rBuf = bytearray(byte)
  wBuf[0] = reg
  i2c.write(0x76, wBuf, False)
  rBuf = i2c.read(0x76, byte, False)
  return rBuf
  
 def i2cReadInt8BE(s, reg):
  rBuf = bytearray(1)
  rBuf = s.i2cRead(reg, 1)
  return rBuf[0]
  
 def i2cReadInt8LE(s, reg):
  rBuf = bytearray(1)
  rBuf = s.i2cRead(reg, 1)
  Rd = s.bit_reverse(rBuf[0])
  return Rd
  
 def i2cReadUInt16LE(s, reg):
  rBuf = bytearray(2)
  rBuf = s.i2cRead(reg, 2)
  val = (0 << 16) | (rBuf[1] << 8) | (rBuf[0])
  return val
  
 def i2cReadInt16LE(s, reg):
  rBuf = bytearray(2)
  rBuf = s.i2cRead(reg, 2)
  val = (rBuf[1] << 8) | rBuf[0]
  return val
 
 def bit_reverse(s, n):
  result = 0
  for i in range (8):
   result <<= 1
   result |= n & 1
   n >>= 1
  return result
 
 def __init__(s): 
  wBuf = bytearray(2)
  wBuf[0] = 0xF2
  wBuf[1] = 0x01
  i2c.write(0x76, wBuf, False) 
  wBuf[0] = 0xF4
  wBuf[1] = 0x2B
  i2c.write(0x76, wBuf, False)
  wBuf[0] = 0xF5
  wBuf[1] = 0x08
  i2c.write(0x76, wBuf, False)
  s._T1 = const(s.i2cReadUInt16LE(0x88))
  s._T2 = const(s.i2cReadInt16LE(0x8A))
  s._T3 = const(s.i2cReadInt16LE(0x8C))
  s._P1 = const(s.i2cReadUInt16LE(0x8E))
  s._P2 = const(s.i2cReadInt16LE(0x90))
  s._P3 = const(s.i2cReadInt16LE(0x92))
  s._P4 = const(s.i2cReadInt16LE(0x94))
  s._P5 = const(s.i2cReadInt16LE(0x96))
  s._P6 = const(s.i2cReadInt16LE(0x98))
  s._P7 = const(s.i2cReadInt16LE(0x9A))
  s._P8 = const(s.i2cReadInt16LE(0x9C))
  s._P9 = const(s.i2cReadInt16LE(0x9E))
  s._H1 = const(s.i2cReadInt8BE(0xA1))
  s._H2 = const(s.i2cReadInt16LE(0xE1))
  s._H3 = const(s.i2cReadInt8BE(0xE3))
  DIG_H4_LSB_DIG_H5_MSB = s.i2cReadInt8BE(0xE5)
  s._H4 = const((s.i2cReadInt8BE(0xE4) << 4) + (DIG_H4_LSB_DIG_H5_MSB % 16))
  s._H5 = const((s.i2cReadInt8BE(0xE6) << 4) + (DIG_H4_LSB_DIG_H5_MSB >> 4))
  s._H6 = const(s.i2cReadInt8LE(0xE7))
 
 def getReadings(s): 
  msrBuf = bytearray(8)
  wBuf = bytearray(1)
  wBuf[0] = 0xF7
  i2c.write(0x76, wBuf, False)
  s.msrBuf = i2c.read(0x76, 8, False)
  s.adcRawPres = ((s.msrBuf[0] << 12) | (s.msrBuf[1] << 4) | ((s.msrBuf[2] & 0xF0) >> 4))
  s.adcRawTemp = ((s.msrBuf[3] << 12) | (s.msrBuf[4] << 4) | ((s.msrBuf[5] & 0xF0) >> 4))
  s.adcRawHumid = ((s.msrBuf[6] << 8) | s.msrBuf[7])
  var1 = (((s.adcRawTemp >> 3) - (s._T1 << 1)) * s._T2) >> 11
  var2 = (((((s.adcRawTemp >> 4) - s._T1) * ((s.adcRawTemp >> 4) - s._T1)) >> 12) * s._T3) >> 14
  s.tempCalc = var1 + var2
  s.tempRead = ((s.tempCalc * 5 + 128) >> 8) / 100
  var1 = (s.tempCalc >> 1) - 64000
  var2 = (((var1 >> 2) * (var1 >> 2)) >> 11) * s._P6
  var2 = var2 + ((var1 * s._P5) << 1)
  var2 = (var2 >> 2) + (s._P4 << 16)
  var1 = (((s._P3 * ((var1 >> 2) * (var1 >> 2)) >> 13) >> 3) + (((s._P2) * var1) >> 1)) >> 18
  var1 = ((32768 + var1) * s._P1) >> 15
  if var1 is 0:
   return
  s.presCalc = ((1048576 - s.adcRawPres) - (var2 >> 12)) * 3125
  s.presCalc = (s.presCalc // var1) * 2
  var1 = (s._P9 * (((s.presCalc >> 3) * (s.presCalc >> 3)) >> 13)) >> 12 
  var2 = ((s.presCalc >> 2) * s._P8) >> 13  
  s.presRead = s.presCalc + ((var1 + var2 + s._P7) >> 4)
  var1 = s.tempCalc - 76800
  var2 = (((s.adcRawHumid << 14) - (s._H4 << 20) - (s._H5 * var1)) + 16384) >> 15
  var1 = var2 * (((((((var1 * s._H6) >> 10) * (((var1 * s._H3) >> 11) + 32768)) >> 10) + 2097152) * s._H2 + 8192) >> 14)
  var2 = var1 - (((((var1 >> 15) * (var1 >> 15)) >> 7) * s._H1) >> 4)
  if var2 < 0:
   var2 = 0
  if var2 > 419430400:
   var2 = 419430400
  s.humidRead = (var2 >> 12) // 1024

 def read(s, readReq): 
  s.getReadings()
  if readReq is "t":
   valRead = s.tempRead
  elif readReq is "p":
   valRead = s.presRead
  elif readReq is "h":
   valRead = s.humidRead
  return valRead
