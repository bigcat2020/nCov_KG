import abc

class NetworkSpider:
    sipdername = 'default'
    @abc.abstractmethod
    def start():
        pass
    def stop():
        pass