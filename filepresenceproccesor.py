import datetime
import time


class FilePresenceProcessor:

    def __init__(self, logger, presence_logger, target, max_disconnect_pings):
        self.logger = logger
        self.presence_logger = presence_logger

        self.target = target

        self.max_disconnect_pings = max_disconnect_pings
        self.presence = False
        self.disconnect_pings = 0

        # Log start message to presence logger
        date_now = datetime.datetime.now()
        date_now_string = date_now.strftime("%Y-%m-%d %H:%M:%S")
        date_now_unixtime = int(time.mktime(date_now.timetuple()))
        msg = "{0} {1} {2}\n".format(date_now_string, date_now_unixtime, "Start")
        self.presence_logger.info(msg)

    @staticmethod
    def __present(answer, address):
        return address in answer

    def __handle_disconnect(self):
        self.disconnect_pings += 1
        if self.disconnect_pings < self.max_disconnect_pings:
            self.logger.debug(
                "Disconnect ping detected {0}/{1}".format(self.disconnect_pings, self.max_disconnect_pings))
        else:
            self.logger.debug(
                "Disconnect ping detected {0}/{1}".format(self.disconnect_pings, self.max_disconnect_pings))
            self.disconnect_pings = 0
            # finally disconnected
            self.presence = False

    def process_scan(self, scan, target):

        self.logger.debug("Processing " + str(scan))

        presence_now = self.__present(scan, target)
        self.logger.debug(presence_now)

        presence_changed = self.presence != presence_now
        if presence_changed:

            # disconnection
            if not presence_now:
                self.__handle_disconnect()

        if presence_now:
            if self.disconnect_pings != 0:
                # connection ok again
                self.logger.debug("Temporal disconnection: Ok now")
                self.disconnect_pings = 0
            self.presence = True

        date_now = datetime.datetime.now()
        date_now_string = date_now.strftime("%Y-%m-%d %H:%M:%S")
        date_now_unixtime = int(time.mktime(date_now.timetuple()))

        presence_updated = presence_changed and self.presence == presence_now
        if presence_updated:
            presence_string = "TARGET FOUND" if self.presence else "TARGET NOT FOUND"
            msg = "{0} {1} {2}\n".format(date_now_string, date_now_unixtime, presence_string)
            self.presence_logger.info(msg)
