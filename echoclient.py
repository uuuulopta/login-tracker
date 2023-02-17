#!/usr/bin/env python
# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.


import logging
from twisted.internet import task
from twisted.internet import reactor
from twisted.internet.defer import Deferred
from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver
import threading
import json
import os
import keyboard

class EchoClient(LineReceiver):
    end = b"Bye-bye!"


    def connectionMade(self):
        machine = os.environ['COMPUTERNAME']
        msg = {"machine" : machine, "name": self.factory.name}
        msg = json.dumps(msg).encode("utf-8")
        if self.factory.target == "professor":
            logging.info("Connected successfully")
            keyboard.unblock_key("enter")
            keyboard.unblock_key("f4")
            keyboard.unblock_key("windows")
            keyboard.unblock_key("ctrl")
            keyboard.unblock_key("alt")
            keyboard.unblock_key("tab")
            self.sendLine(msg)
            self.factory.closeScreen = True
        if self.factory.target == "mainServer":
            self.sendLine(msg)
            self.transport.loseConnection()
    def connectionLost(self, reason):

        print("Connection lost !")

    def lineReceived(self, line):
        print(line)
        if line == b"lock" :
            logging.info("Recieved lock command. Disconnecting...")
            self.factory.closeScreen = False
            self.transport.loseConnection()
    def dataReceived(self, data):
        print(data)
        if data == b"lock" :
            logging.info("Recieved lock command. Disconnecting...")
            print("Recieved lock command. Disconnecting...")
            self.factory.closeScreen = False
            self.transport.loseConnection()


class EchoClientFactory(ClientFactory):
    """
    Create a twisted factory for the EchoClient protcol
    
    Paramaters
    ----------
    name(string) : Studen's name
    target(string) : Target either professor or main server (defualt -> professor) (Optional)
    """
    protocol = EchoClient
    closeScreen = True
    
    def __init__(self,name,target="professor"):
        self.done = Deferred()
        self.name = name
        self.target = target
    def clientConnectionFailed(self, connector, reason):
        if self.target == "professor":
            print("connection failed:", reason.getErrorMessage())
            logging.info(f"Connection failed {reason.getErrorMessage()!r}")
            self.done.errback(reason)
            reactor.stop()
    def clientConnectionLost(self, connector, reason):
        if self.target == "professor":
            logging.info(f"Connection lost with the professor server {reason.getErrorMessage()!r}")
        
        if self.target == "mainServer":
            logging.info(f"Connection lost with the main server {reason.getErrorMessage()!r}")
        
        print("connection lost:", reason.getErrorMessage())
        
        if self.closeScreen and self.target == "professor":
            reactor.stop()



