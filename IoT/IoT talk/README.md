IoT talk : sensor,device and model
========
### What is IoT talk system ?

The IoT talk system is create by Jason Yi-Bing Lin[1].
It is a useful IoT connection system that can used easily.
Just by using the website GUI and some python code,
we can built a system that contains sensing,visualization, prediction and spraying the water due to 
prediction result.And the codes we used are shown above.<br />
#### Note!!!
##### The IoT talk system from Yi-Bing Lin's lab is not release yet. 
##### So it doesn`t allow other peoples to use.
##### To see our result , you can watch the video in our wiki [IoT demo](http://2017.igem.org/Team:NCTU_Formosa/Demonstrate)

Sensor&spraying
--------
The `iot_sensor.ino` is a part of our IoT talk system that can sensing the weather information,
such as temperature,humidity,pressure and rainfall. After that,the device will send these data to the
 IoT talk server.

These libraries are requested of running this code.
```
<Bridge.h>
<BridgeClient.h>
<BridgeServer.h>
<BridgeSSLClient.h>
<BridgeUdp.h>
<Console.h>
<FileIO.h>
<HttpClient.h>
<Mailbox.h>
<Process.h>
<YunClient.h>
<YunServer.h>
<excel.h>
<SimpleDHT.h>
<Wire.h>
<Adafruit_BMP085_U.h>
<Adafruit_Sensor.h>
<SoftwareSerial.h>
<math.h>
<SPI.h>
```

Visualization
--------
The `web.py` is a part of our IoT talk system that can show weather data from sensor by ThingSpeak.
It is a free website that can be easily used.

These libraries are requested of running this code.

`python3.6` with following packages `requests`.

Device
--------
The `Data_model.py` is our IoT talk prediction model,
it can store the data from sensor and run the prediction model everyday.
These libraries are requested of running this code.

`python3.6` with following packages `requests`,`sqlite3`,`numpy`,`tensorflow` and `tensorlayer`.
`DAN.py` and `sql_io.py` are some packages that required for IoT talk connecting and sqlite I/O.


#### Reference : 
[1]Y. W. Lin, Y. B. Lin, C. Y. Hsiao and Y. Y. Wang, "IoTtalk-RC: Sensors As Universal Remote Control for Aftermarket Home Appliances," in IEEE Internet of Things Journal, vol. 4, no. 4, pp. 1104-1112, Aug. 2017.
doi: 10.1109/JIOT.2017.2715859