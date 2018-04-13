# BluePing

Simple bluetooth tracker implemented using Python 3

This is just a demo to raise awareness on the dangers of having periocal-beaconing devices such as current wearable fitness tracker. 
They can be easily used to track us.  
The program tracks the presence of a target device identified by a unique address (MAC address in the case of Bluetooth) 

The program uses dependency injection

# Installation

1. pip install -r requirements (if you have problems in windows you might need to install a newer version of pip. E.g.: 10.0.0.dev0)
2. Connect HM-10 to a serial using for example a xbee explorer (gnd, vcc, tx and rx)
3. Make sure AT+ROLE and and AT+IMME are set to 1 in HM-10 (central bluetooth role)

# Execute

* Modify config inside blueping.py
    * Serial com where bluetooth is connected, baudrate, etc

* Run tracker: py blueping.py

* Run server : py server.py

* Go to: localhost:8066/key


# Implementation

The demo uses a TinySine bluetooth module (HM-10) to periodically scan for nearby devicies in order to detect the target device and log its presence


# Dependencies

1. dependency_injector
2. pyserial

# Disclaimer

 No need to clarify anything. The title says it all
