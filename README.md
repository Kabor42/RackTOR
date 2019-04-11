RackTOR
================

This project uses some **DS18S20** digital temperature sensors to get temperature data.

Data
----

The data between the Arduino and RasPI flows like this:
1. Arduino reads sensors every second, and displays temperature on the LCD.
1. Python scripts sends out control sequence `c7` to get data from Arduino.
1. Arduino sends it's custom **ID, sensorPin, device, temperature** each on a separate line.

|Type| Descirption|
|----|-------------|
|**ID**| Is a 4 digit code. For I2C interface can be between 1000-1127.|
|**SensorPin**| Is the pin where the OneWire reads data. Could be any of the digitalIOs.|
|**Device**| Number of the device on the OneWire interface. 0-127.|
|**Temperature**| Float value. Usually 2 decimal places. range could be -25 - +125. |

There's a cronjob running on the system, which pulls data from devices every 5 minutes. 
It could be set to almost any value. 

The python script automatically reads data from Arduino, and should convert it to JSON-format.
JSON is needed to pass data to InfluxDB by the influxdb-python module. 
Then Grafana reads its data from InfluxDB.


Grafana
-------


```bash
sudo systemctl daemon-reload
sudo systemctl start grafana-server
sudo systemctl status grafana-server
```

* **Binaries** `/usr/sbin/grafana-server`
* **Init.d** `/etc/init.d/grafana-server`
* **ENV vars** `/etc/default/grafana-server`
* **CONF** `/etc/grafana/grafana.ini`
* **Systemd** `grafana-server.service`
* **LOG** `/var/log/grafana/grafana.db`
* **DB** `/var/lib/grafana/grafana.db`
* **HTML/JS/CSS** `/usr/share/grafana`

Default port is **3000**, default user **admin** and password **admin**.

Changed password to `racktor`.

