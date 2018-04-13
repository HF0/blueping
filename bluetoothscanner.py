import logging
import serial


class BluetoothTinySineScanner:

    def __init__(self, logger, port, baudrate, serial_timeout_seconds):
        self.logger = logger

        self.port = port
        self.baudrate = serial
        self.serial_timeout_seconds = serial_timeout_seconds

        self.logger.debug("Opening serial {0} {1}".format(port, baudrate))
        try:
            self.serial = serial.Serial(port, baudrate, timeout=serial_timeout_seconds)
        except serial.serialutil.SerialException:
            self.logger.error("Could not open {} {}".format(port, baudrate))

    def scan(self):
        self.logger.debug("scanning...")
        self.__send("AT+DISC?")
        answer = self.serial.read(100)
        answerAscii = answer.decode("ascii")
        #example: OK+DISCSOK+DIS0:123456789012OK+DISCE
        # parse answer
        tags = answerAscii.split("OK+DIS")
        list = []
        for tag in tags:
            if ":" in tag:
                addr = tag.split(":")[1]
                list.append(addr)
        
        self.logger.debug("scan finished")
        return list

    def __send(self, data):
        data_to_send = (data).encode('ascii')
        self.logger.debug("Sending {0} {1}".format(data_to_send, len(data_to_send)))
        self.serial.write(data_to_send)
        data.rstrip()
        self.logger.debug(data)


if __name__ == "__main__":

    loggertest = logging.getLogger()
    loggertest.setLevel(logging.DEBUG)
    logFormatter = logging.Formatter("%(asctime)s %(message)s")
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    loggertest.addHandler(consoleHandler)
    loggertest.info("Init test")

    bt = BluetoothTinySineScanner(loggertest, "com4", 115200, 30)
    loggertest.info("Scanning...")
    identities = bt.scan()
    loggertest.info("Result {}".format(identities))
    
    
    