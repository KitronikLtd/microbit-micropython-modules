# microbit-module: kitronikRTC@0.0.1
# A module for the Kitronik RTC chip
from microbit import i2c
from microbit import pin19
from microbit import pin20

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
    RTC_OSCILLATOR_REG = 0x08
    RTC_PWR_UP_MINUTE_REG = 0x1C
    START_RTC = 0x80
    STOP_RTC = 0x00
    ENABLE_BATTERY_BACKUP = 0x08
    currentSeconds = 0
    currentMinutes = 0
    currentHours = 0
    currentWeekDay = 0
    currentDay = 0
    currentMonth = 0
    currentYear = 0

    def __init__(self):
        i2c.init(freq=100000, sda=pin20, scl=pin19)
        writeBuf = bytearray(2)
        readBuf = bytearray(1)
        readCurrentSeconds = 0
        readWeekDayReg = 0
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
        tens = 0
        units = 0
        bcdNumber = 0
        tens = decNumber // 10
        units = decNumber % 10
        bcdNumber = (tens << 4) | units
        return bcdNumber

    def bcdToDec(self, bcdNumber, readReg):
        mask = 0
        if readReg is self.RTC_SECONDS_REG:
            mask = 0x70
        elif readReg is self.RTC_MINUTES_REG:
            mask = 0x70
        elif readReg is self.RTC_DAY_REG:
            mask = 0x30
        elif readReg is self.RTC_HOURS_REG:
            mask = 0x10
        elif readReg is self.RTC_MONTH_REG:
            mask = 0x10
        elif readReg is self.RTC_YEAR_REG:
            mask = 0xF0
        units = bcdNumber & 0x0F
        tens = bcdNumber & mask
        shiftedTens = tens >> 4
        decNumber = (shiftedTens * 10) + units
        print(decNumber)
        return decNumber

    def readValue(self): 
        writeBuf = bytearray(1)
        readBuf = bytearray(7)
        self.readCurrentSeconds = 0
        writeBuf[0] = self.RTC_SECONDS_REG
        i2c.write(self.CHIP_ADDRESS, writeBuf, False)
        readBuf = i2c.read(self.CHIP_ADDRESS, 7, False)
        self.currentSeconds = readBuf[0]
        self.currentMinutes = readBuf[1]
        self.currentHours = readBuf[2]
        self.currentWeekDay = readBuf[3]
        self.currentDay = readBuf[4]
        self.currentMonth = readBuf[5]
        self.currentYear = readBuf[6]

    def readTime(self, readRequest): 
        timeRead=0
        self.readValue()
        if readRequest is "hours":
            timeRead = self.bcdToDec(self.currentHours, self.RTC_HOURS_REG)
        elif readRequest is "minutes":
            timeRead = self.bcdToDec(self.currentMinutes, self.RTC_MINUTES_REG)
        elif readRequest is "seconds":
            timeRead = self.bcdToDec(self.currentSeconds, self.RTC_SECONDS_REG)
        return timeRead

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