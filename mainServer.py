from twisted.internet import reactor
from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
import json
import logging
import logging.handlers
class Chat(LineReceiver):
    def __init__(self):
        self.name = None
        self.machine = None
    def connectionMade(self):
        pass
    def connectionLost(self,reason):
        pass
    def lineReceived(self, data):
        msg = data.decode()
        msg = json.loads(msg)
        logging.info(msg)

class ChatFactory(Factory):
    locking = False
    clientMap = {}
    def __init__(self):
        self.connections = {}  # maps user names to Chat instances

    def buildProtocol(self, addr):
        # I thought factory gets passed on its own like in the server, but I gues not... ?
        protocol = Chat()
        protocol.factory = self
        return protocol



if __name__ == "__main__":
    rfh = logging.handlers.RotatingFileHandler(
        filename='mainServerLogger.txt',
        mode='a',
        maxBytes=100 * 1024 * 1024,
        backupCount=2,
        encoding="utf-8",
        delay=0
    )
    logging.basicConfig(handlers=[rfh], level=logging.DEBUG,
                        format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')

    factory = ChatFactory()
    f = open("mainServerConfig.json") 
    data = json.load(f)
    port = data["port"]
    f.close()
    reactor.listenTCP(port, factory)
    logging.info(f"Listening on {port} ")
    reactor.run()