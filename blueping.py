import datetime
import logging
import sys
import time
import traceback

from containers import Core, Services
from bluetoothscanner import BluetoothTinySineScanner
import dependency_injector.providers as providers

Core.config.override(
    dict(
        target='id1',
        max_disconnect_pings=5,
		period = 5,
        presence={'filename': 'blueping.txt'},

        bluetoothtinysinescanner={
            'port' : 'com14',
            'baudrate' : 115200,
            'serial_timeout_seconds' : 30
        }

    ))


# configure logger
Core.logger().setLevel(logging.DEBUG)
logFormatter = logging.Formatter("%(asctime)s %(message)s")
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
Core.logger().addHandler(consoleHandler)
dateTag = datetime.datetime.now().strftime("%Y-%b-%d_%H-%M-%S")
fileHandler = logging.FileHandler("{0}-{1}.txt".format("log", dateTag))
fileHandler.setFormatter(logFormatter)
Core.logger().addHandler(fileHandler)

# configure presence logger
Core.presence_logger().setLevel(logging.INFO)
presenceFileHandler = logging.FileHandler(Core.config.presence.filename())
presenceFileHandler.setFormatter(logFormatter)
Core.presence_logger().addHandler(presenceFileHandler)


# scan identities from bluetooth
Services.identity_scanner.override(
    providers.Singleton(BluetoothTinySineScanner,
       logger=Core.logger(),
       port=Core.config.bluetoothtinysinescanner.port,
       baudrate=Core.config.bluetoothtinysinescanner.baudrate,
       serial_timeout_seconds=Core.config.bluetoothtinysinescanner.serial_timeout_seconds))

try:

    while True:
        
            identities = Services.identity_scanner().scan()
            Services.presence_processor().process_scan(identities, Core.config.target())
            time.sleep(Core.config.period())
        
except Exception as e:
    Core.logger().debug("Error:" + str(e))
    traceback.print_exc(file=sys.stdout)
