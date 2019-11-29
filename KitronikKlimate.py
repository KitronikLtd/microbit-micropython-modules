# microbit-module: kitronikKlimate@0.0.1
from microbit import *

class Klimate:
    global temperatureReading	
    global pressureReading
    global humidityReading
    global T1
    global T2
    global T3
    global P1
    global P2
    global P3
    global P4
    global P5
    global P6
    global P7
    global P8
    global P9
    global H1
    global H2
    global H3
    global H4
    global H5
    global H6
    global adcRawTemperature       
    global adcRawPressure       
    global adcRawHumidity       

    def i2cRead(self, reg, byte):
        writeBuf = bytearray(1)
        readBuf = bytearray(byte)
        writeBuf[0] = reg
        i2c.write(0x76, writeBuf, False)
        readBuf = i2c.read(0x76, byte, False)
        return readBuf
        
    def i2cReadInt8BE(self, reg):
        readBuf = bytearray(1)
        readBuf = self.i2cRead(self, reg, 1)
        return readBuf[0]
        
    def i2cReadInt8LE(self, reg):
        readBuf = bytearray(1)
        readBuf = self.i2cRead(self, reg, 1)
        Rd = self.bit_reverse(readBuf[0])
        return Rd
        
    def i2cReadUInt16LE(self, reg):
        readBuf = bytearray(2)
        readBuf = self.i2cRead(self, reg, 2)
        value = (0 << 16) | (readBuf[1] << 8) | (readBuf[0])
        return value
        
    def i2cReadInt16LE(self, reg):
        readBuf = bytearray(2)
        readBuf = self.i2cRead(self, reg, 2)
        value = (readBuf[1] << 8) | readBuf[0]
        return value
    
    def bit_reverse(n):
        result = 0
        for i in range (8):
            result <<= 1
            result |= n & 1
            n >>= 1
        return result
    
    def secretIncantation(self): 
        writeBuf = bytearray(2)
        writeBuf[0] = 0xF2
        writeBuf[1] = 0x01
        i2c.write(0x76, writeBuf, False) 
        writeBuf[0] = 0xF4
        writeBuf[1] = 0x2B
        i2c.write(0x76, writeBuf, False)
        writeBuf[0] = 0xF5
        writeBuf[1] = 0x08
        i2c.write(0x76, writeBuf, False)
        self.T1 = self.i2cReadUInt16LE(self, 0x88)
        self.T2 = self.i2cReadInt16LE(self, 0x8A)
        self.T3 = self.i2cReadInt16LE(self, 0x8C)
        self.P1 = self.i2cReadUInt16LE(self, 0x8E)
        self.P2 = self.i2cReadInt16LE(self, 0x90)
        self.P3 = self.i2cReadInt16LE(self, 0x92)
        self.P4 = self.i2cReadInt16LE(self, 0x94)
        self.P5 = self.i2cReadInt16LE(self, 0x96)
        self.P6 = self.i2cReadInt16LE(self, 0x98)
        self.P7 = self.i2cReadInt16LE(self, 0x9A)
        self.P8 = self.i2cReadInt16LE(self, 0x9C)
        self.P9 = self.i2cReadInt16LE(self, 0x9E)
        self.H1 = self.i2cReadInt8BE(self, 0xA1)
        self.H2 = self.i2cReadInt16LE(self, 0xE1)
        self.H3 = self.i2cReadInt8BE(self, 0xE3)
        DIG_H4_LSB_DIG_H5_MSB = self.i2cReadInt8BE(self, 0xE5)
        self.H4 = (self.i2cReadInt8BE(self, 0xE4) << 4) + (DIG_H4_LSB_DIG_H5_MSB % 16)
        self.H5 = (self.i2cReadInt8BE(self, 0xE6) << 4) + (DIG_H4_LSB_DIG_H5_MSB >> 4)
        self.H6 = self.i2cReadInt8LE(self, 0xE7)
    
    def getReadings(self): 
        measurementsBuf = bytearray(8)
        writeBuf = bytearray(1)
        writeBuf[0] = 0xF7
        i2c.write(0x76, writeBuf, False)
        self.measurementsBuf = i2c.read(0x76, 8, False)
        self.adcRawPressure = ((self.measurementsBuf[0] << 12) | (self.measurementsBuf[1] << 4) | ((self.measurementsBuf[2] & 0xF0) >> 4))
        self.adcRawTemperature = ((self.measurementsBuf[3] << 12) | (self.measurementsBuf[4] << 4) | ((self.measurementsBuf[5] & 0xF0) >> 4))
        self.adcRawHumidity = ((self.measurementsBuf[6] << 8) | self.measurementsBuf[7])
        var1 = (((self.adcRawTemperature >> 3) - (self.T1 << 1)) * self.T2) >> 11
        var2 = (((((self.adcRawTemperature >> 4) - self.T1) * ((self.adcRawTemperature >> 4) - self.T1)) >> 12) * self.T3) >> 14
        self.temperatureCalculation = var1 + var2
        self.temperatureReading = ((self.temperatureCalculation * 5 + 128) >> 8) / 100
        var1 = (self.temperatureCalculation >> 1) - 64000
        var2 = (((var1 >> 2) * (var1 >> 2)) >> 11) * self.P6
        var2 = var2 + ((var1 * self.P5) << 1)
        var2 = (var2 >> 2) + (self.P4 << 16)
        var1 = (((self.P3 * ((var1 >> 2) * (var1 >> 2)) >> 13) >> 3) + (((self.P2) * var1) >> 1)) >> 18
        var1 = ((32768 + var1) * self.P1) >> 15
        if var1 is 0:
            return
        self.pressureCalculation = ((1048576 - self.adcRawPressure) - (var2 >> 12)) * 3125
        self.pressureCalculation = (self.pressureCalculation // var1) * 2
        var1 = (self.P9 * (((self.pressureCalculation >> 3) * (self.pressureCalculation >> 3)) >> 13)) >> 12 
        var2 = ((self.pressureCalculation >> 2) * self.P8) >> 13     
        self.pressureReading = self.pressureCalculation + ((var1 + var2 + self.P7) >> 4)
        var1 = self.temperatureCalculation - 76800
        var2 = (((self.adcRawHumidity << 14) - (self.H4 << 20) - (self.H5 * var1)) + 16384) >> 15
        var1 = var2 * (((((((var1 * self.H6) >> 10) * (((var1 * self.H3) >> 11) + 32768)) >> 10) + 2097152) * self.H2 + 8192) >> 14)
        var2 = var1 - (((((var1 >> 15) * (var1 >> 15)) >> 7) * self.H1) >> 4)
        if var2 < 0:
            var2 = 0
        if var2 > 419430400:
            var2 = 419430400
        self.humidityReading = (var2 >> 12) // 1024

    def readValue(self): 
        self.getReadings(self)
        temperatureStr = str(self.temperatureReading)
        humidityStr = str(self.humidityReading)
        pressureStr = str(self.pressureReading)
        parameterStr = "" + (temperatureStr) + "C  " + (pressureStr) + "Pa  " + (humidityStr) + "%"
        return parameterStr
