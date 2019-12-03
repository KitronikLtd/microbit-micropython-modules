# microbit-module: kitronikRTC@0.0.1
# A module for the Kitronik RTC chip
from microbit import i2c, pin19, pin20

class RTC:
    def __init__(self):
        i2c.init(freq=100000, sda=pin20, scl=pin19)
        writeBuf = bytearray(2)
        readBuf = bytearray(1)
        writeBuf[0] = 0x00
        i2c.write(0x6F, writeBuf, False)
        readBuf = i2c.read(0x6F, 1, False)
        readCurrentSeconds = readBuf[0]
        writeBuf[0] = 0x07
        writeBuf[1] = 0x43
        i2c.write(0x6F, writeBuf, False)
        writeBuf[0] = 0x03
        i2c.write(0x6F, writeBuf, False)
        readBuf = i2c.read(0x6F, 1, False)
        readWeekDayReg = readBuf[0]
        writeBuf[0] = 0x03
        writeBuf[1] = 0x08 | readWeekDayReg
        i2c.write(0x6F, writeBuf, False)
        writeBuf[0] = 0x00
        writeBuf[1] = 0x80 | readCurrentSeconds
        i2c.write(0x6F, writeBuf, False)

    def decToBcd(self, decNumber):
        tens = decNumber // 10
        units = decNumber % 10
        bcdNumber = (tens << 4) | units
        return bcdNumber

    def bcdToDec(self, bcdNumber, mask):
        units = bcdNumber & 0x0F
        tens = bcdNumber & mask
        shiftedTens = tens >> 4
        decNumber = (shiftedTens * 10) + units
        return decNumber

    def read(self, readRequest): 
        writeBuf = bytearray(1)
        readBuf = bytearray(7)
        writeBuf[0] = 0x00
        i2c.write(0x6F, writeBuf, False)
        readBuf = i2c.read(0x6F, 7, False)
        currentSeconds = readBuf[0]
        currentMinutes = readBuf[1]
        currentHours = readBuf[2]
        currentWeekDay = readBuf[3]
        currentDay = readBuf[4]
        currentMonth = readBuf[5]
        currentYear = readBuf[6]

        if readRequest is "hours":
            valueRead = self.bcdToDec(currentHours, 0x10)
        elif readRequest is "minutes":
            valueRead = self.bcdToDec(currentMinutes, 0x70)
        elif readRequest is "seconds":
            valueRead = self.bcdToDec(currentSeconds, 0x70)
        elif readRequest is "day":
            valueRead = self.bcdToDec(currentDay, 0x30)
        elif readRequest is "month":
            valueRead = self.bcdToDec(currentMonth, 0x10)
        elif readRequest is "year":
            valueRead = self.bcdToDec(currentYear, 0xF0)
        return valueRead

    def setTime(self, setHours, setMinutes, setSeconds): 
        bcdHours = self.decToBcd(setHours)
        bcdMinutes = self.decToBcd(setMinutes)
        bcdSeconds = self.decToBcd(setSeconds)
        writeBuf = bytearray(2)
        writeBuf[0] = 0x00
        writeBuf[1] = 0x00
        i2c.write(0x6F, writeBuf, False)
        writeBuf[0] = 0x02
        writeBuf[1] = bcdHours	
        i2c.write(0x6F, writeBuf, False)
        writeBuf[0] = 0x01
        writeBuf[1] = bcdMinutes
        i2c.write(0x6F, writeBuf, False)
        writeBuf[0] = 0x00
        writeBuf[1] = 0x80 | bcdSeconds
        i2c.write(0x6F, writeBuf, False)

    def setDate(self, setDay, setMonth, setYear): 
        writeBuf = bytearray(2)
        readBuf = bytearray(1)
        if setMonth is 4 or 6 or 9 or 11:
            if setDay >= 30:
                setDay = 30
        if setMonth is 2 and setDay >= 29:
            leapYearCheck = setYear % 4
            if leapYearCheck is 0:
                setDay = 29
            else:
                setDay = 28
        bcdDay = self.decToBcd(setDay)
        bcdMonths = self.decToBcd(setMonth)
        bcdYears = self.decToBcd(setYear)
        writeBuf[0] = 0x00
        i2c.write(0x6F, writeBuf, False)
        readBuf = i2c.read(0x6F, 1, False)
        readCurrentSeconds = readBuf[0]
        writeBuf[0] = 0x00
        writeBuf[1] = 0x00
        i2c.write(0x6F, writeBuf, False)
        writeBuf[0] = 0x04
        writeBuf[1] = bcdDay
        i2c.write(0x6F, writeBuf, False)
        writeBuf[0] = 0x05
        writeBuf[1] = bcdMonths
        i2c.write(0x6F, writeBuf, False)
        writeBuf[0] = 0x06
        writeBuf[1] = bcdYears
        i2c.write(0x6F, writeBuf, False)
        writeBuf[0] = 0x00
        writeBuf[1] = 0x80 | readCurrentSeconds
        i2c.write(0x6F, writeBuf, False)