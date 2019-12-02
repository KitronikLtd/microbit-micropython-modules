# microbit-module: kitronikRTC@0.0.1
# A module for the Kitronik RTC chip
from microbit import i2c, pin19, pin20

class RTC:
    CHIP_ADDRESS = 0x6F
    RTC_SECONDS_REG = 0x00
    RTC_MINUTES_REG = 0x01
    RTC_HOURS_REG = 0x02
    RTC_WEEKDAY_REG = 0x03
    RTC_DAY_REG = 0x04
    RTC_MONTH_REG = 0x05
    RTC_YEAR_REG = 0x06
    RTC_CONTROL_REG = 0x07
    START_RTC = 0x80
    STOP_RTC = 0x00
    ENABLE_BATTERY_BACKUP = 0x08

    def __init__(self):
        i2c.init(freq=100000, sda=pin20, scl=pin19)
        writeBuf = bytearray(2)
        readBuf = bytearray(1)
        writeBuf[0] = self.RTC_SECONDS_REG
        i2c.write(self.CHIP_ADDRESS, writeBuf, False)
        readBuf = i2c.read(self.CHIP_ADDRESS, 1, False)
        readCurrentSeconds = readBuf[0]
        writeBuf[0] = self.RTC_CONTROL_REG
        writeBuf[1] = 0x43
        i2c.write(self.CHIP_ADDRESS, writeBuf, False)
        writeBuf[0] = self.RTC_WEEKDAY_REG
        i2c.write(self.CHIP_ADDRESS, writeBuf, False)
        readBuf = i2c.read(self.CHIP_ADDRESS, 1, False)
        readWeekDayReg = readBuf[0]
        writeBuf[0] = self.RTC_WEEKDAY_REG
        writeBuf[1] = self.ENABLE_BATTERY_BACKUP | readWeekDayReg
        i2c.write(self.CHIP_ADDRESS, writeBuf, False)
        writeBuf[0] = self.RTC_SECONDS_REG
        writeBuf[1] = self.START_RTC | readCurrentSeconds
        i2c.write(self.CHIP_ADDRESS, writeBuf, False)

    def decToBcd(self, decNumber):
        tens = decNumber // 10
        units = decNumber % 10
        bcdNumber = (tens << 4) | units
        return bcdNumber

    def bcdToDec(self, mask, bcdNumber):
        units = bcdNumber & 0x0F
        tens = bcdNumber & mask
        shiftedTens = tens >> 4
        decNumber = (shiftedTens * 10) + units
        return decNumber
        
    def read(self, readRequest): 
        writeBuf = bytearray(1)
        readBuf = bytearray(7)
        writeBuf[0] = self.RTC_SECONDS_REG
        i2c.write(self.CHIP_ADDRESS, writeBuf, False)
        readBuf = i2c.read(self.CHIP_ADDRESS, 7, False)
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
        writeBuf[0] = self.RTC_SECONDS_REG
        writeBuf[1] = self.STOP_RTC
        i2c.write(self.CHIP_ADDRESS, writeBuf, False)
        writeBuf[0] = self.RTC_HOURS_REG
        writeBuf[1] = bcdHours	
        i2c.write(self.CHIP_ADDRESS, writeBuf, False)
        writeBuf[0] = self.RTC_MINUTES_REG
        writeBuf[1] = bcdMinutes
        i2c.write(self.CHIP_ADDRESS, writeBuf, False)
        writeBuf[0] = self.RTC_SECONDS_REG
        writeBuf[1] = self.START_RTC | bcdSeconds
        i2c.write(self.CHIP_ADDRESS, writeBuf, False)

    def setDate(self, setDay, setMonth, setYear): 
        writeBuf = bytearray(2)
        readBuf = bytearray(1)
        if setMonth is 4 or 6 or 9 or 11:
            if setDay is 30:
                setDay = 30
        if setMonth is 2 and setDay is 29:
            leapYearCheck = setYear % 4
            if leapYearCheck is 0:
                setDay = 29
            else:
                setDay = 28
        bcdDay = self.decToBcd(setDay)
        bcdMonths = self.decToBcd(setMonth)
        bcdYears = self.decToBcd(setYear)
        writeBuf[0] = self.RTC_SECONDS_REG
        i2c.write(self.CHIP_ADDRESS, writeBuf, False)
        readBuf = i2c.read(self.CHIP_ADDRESS, 1, False)
        readCurrentSeconds = readBuf[0]
        writeBuf[0] = self.RTC_SECONDS_REG
        writeBuf[1] = self.STOP_RTC
        i2c.write(self.CHIP_ADDRESS, writeBuf, False)
        writeBuf[0] = self.RTC_DAY_REG
        writeBuf[1] = bcdDay
        i2c.write(self.CHIP_ADDRESS, writeBuf, False)
        writeBuf[0] = self.RTC_MONTH_REG
        writeBuf[1] = bcdMonths
        i2c.write(self.CHIP_ADDRESS, writeBuf, False)
        writeBuf[0] = self.RTC_YEAR_REG
        writeBuf[1] = bcdYears
        i2c.write(self.CHIP_ADDRESS, writeBuf, False)
        writeBuf[0] = self.RTC_SECONDS_REG
        writeBuf[1] = self.START_RTC | readCurrentSeconds
        i2c.write(self.CHIP_ADDRESS, writeBuf, False)