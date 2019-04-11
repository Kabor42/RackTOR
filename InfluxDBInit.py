#!/usr/bin/env python3
from influxdb import InfluxDBClient

'''
InfluxDB database initialization
'''

client = InfluxDBClient('localhost', 8086, 'root', 'root', 'racktor')
client.create_database('racktor')
client.create_user('racktor', 'racktor')
client.grant_privilege('all', 'racktor', 'racktor')
client.close()