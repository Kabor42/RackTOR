#!/usr/bin/env python3
import serial
import time
import datetime
from influxdb import InfluxDBClient

'''
Serial --> Serial communication via USB.
           Can be changed to I2C later.
time   --> For waiting.
datetime > Real time timestamp. FOr influxDB
'''

'''
@class AruduinoData
@param ID Arduino device identification.
@param wire arduino sensor one wire interface number.
@param dev one wire interface device, 0-127.
@see OneWire interface

This class represents the data read from the arduino device.
Always initialize when reading from the device. @see __init__.

In the future could be upgraded to differentiate between analog and digital.
Also a method to read the data from serial connection.
'''
class ArduinoData:
    '''
    Main initialization function.
    Nothing fancy.
    Creates timestamp when created.
    '''
    def __init__(self, ID, wire, dev, temp):
        self.ID = ID
        self.wire = wire
        self.dev = dev
        self.temp = temp
        self.tm = str(datetime.datetime.now().isoformat('T'))
    '''
    Converts wire and dev number to a dotted format.
    '''
    def region(self):
        return "{}.{}".format(self.wire, self.dev)
    '''
    Converts class to a JSON format.
    Use with InfluxDB.
    '''
    def toJSON(self):
        body = {"measurement":"RackTemp","tags":{"host":self.ID,"region":self.region()},
                 "time":self.tm,"fields":{"value":self.temp}}
        return body
    '''
    String representation for debugging.
    '''
    def __str__(self):
        return "{}_{}.{}_{}°C_{}".format(self.ID,
                                          self.wire,
                                          self.dev,
                                          self.temp,
                                          self.tm)
    '''
    String representation for debugging.
    '''
    def __repr__(self):
        return "ID: {}\nRegion: {}.{}\nTemp: {}°C\nTime: {}\n".format(
            self.ID,
            self.wire, self.dev,
            self.temp, self.tm)


'''
Reads data from the Android device at comPort.
@param comPort Android connection.
@returns new ArduinoData object.

The flow is the following.
Send control sequence 'c7' to Arduino.
Read device ID, wire, device and temperature,
each in a new line.
'''
def getDataFromDevice( comPort ):
    Arduino = serial.Serial( comPort, 9600, timeout=1)
    command = "c7\r\n"
    Arduino.write(command.encode())
    time.sleep(1)
    data = ArduinoData(
        int(Arduino.readline().decode()),
        int(Arduino.readline().decode()),
        int(Arduino.readline().decode()),
        float(Arduino.readline().decode())
    )
    Arduino.close()
    return data

port = '/dev/ttyACM0'
data = getDataFromDevice(port)

with open('/mnt/STORAGE/arduino.json', 'a') as jsonFile:
    jsonFile.write(str(data.toJSON())+",\n")

client = InfluxDBClient('localhost', 8086, 'racktor', 'racktor', 'racktor')
client.write_points(data.toJSON())