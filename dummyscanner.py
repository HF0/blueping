
class DummyScanner:


    def __init__(self, logger):
        self.logger = logger
        self.__state = 0

    def scan(self):
        self.logger.info("scanned")
        res = ["id1", "id2"] if self.__state == 0 else []
        self.__state += 1
        self.__state %= 8
        return res

