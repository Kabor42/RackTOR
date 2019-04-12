#!/usr/bin/env python3
import serial
import time
import datetime
from influxdb import InfluxDBClient
from influxdb import SeriesHelper

"""
Serial --> Serial communication via USB.
Can be changed to I2C later.
time   --> For waiting.
datetime > Real time timestamp. FOr influxDB
"""

DB_client = InfluxDBClient('localhost', 8086, 'racktor', 'racktor', 'racktor')

class MySeriesHelper(SeriesHelper):
    class Meta:
        client = DB_client
        series_name = 'temperature'
        fields = ['temp']
        tags = ['host', 'region']
        bulk_size = 3
        autocommit = True

class ArduinoData:
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
    def __init__(self, ID, wire, dev, temp):
        """
        Main initialization function.
        Nothing fancy.
        Creates timestamp when created.
        """
        self.ID = ID
        self.wire = wire
        self.dev = dev
        self.temp = temp
        self.tm = str(datetime.datetime.now().isoformat('T'))

    def region(self):
        """ Converts wire and dev number to a dotted format. """   
        return "{}.{}".format(self.wire, self.dev)
    def __str__(self):
        return "{}_{}.{}_{}°C_{}".format(self.ID,
                                          self.wire,
                                          self.dev,
                                          self.temp,
                                          self.tm)
    def __repr__(self):
        return "ID: {}\nRegion: {}.{}\nTemp: {}°C\nTime: {}\n".format(
            self.ID,
            self.wire, self.dev,
            self.temp, self.tm)
    def toSeries(self):
        return MySeriesHelper(temp=self.temp, region=self.region(), host=self.ID)


def getDataFromDevice( comPort ):
    """
    Reads data from the Android device at comPort.
    @param comPort Android connection.
    @returns new ArduinoData object.

    The flow is the following.
    Send control sequence 'c7' to Arduino.
    Read device ID, wire, device and temperature,
    each in a new line.
    """
    Arduino = serial.Serial( comPort, 9600, timeout=1)
    command = "c7\r\n"
    Arduino.write(command.encode())
    time.sleep(1)
    data = ArduinoData(
        "A" + str(int(Arduino.readline().decode())),
        "rack" + str(int(Arduino.readline().decode())),
        "region" + str(int(Arduino.readline().decode())),
        float(Arduino.readline().decode())
    )
    Arduino.close()
    return data

port = '/dev/ttyACM0'
data = getDataFromDevice(port)

myHelper = data.toSeries()
if not myHelper.commit():
    print("Error during data commit!")
