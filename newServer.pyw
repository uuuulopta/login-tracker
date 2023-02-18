import threading
import time
from tkinter import *
import asyncio
import logging
from logging import handlers
import json
from tkinter import messagebox
import os
from echoserv import Chat,ChatFactory
from twisted.internet import reactor
from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from PIL import ImageTk, Image

def restart():
    if not factory.locking:
        factory.lock()

def onClosing():
    os._exit(0)
def runLoop():
    window = Tk()
    # window.attributes('-fullscreen', True)
    parent = Frame(window)
    parent.pack(expand=1)  # same as expand=True
    L_connections = StringVar()
    L_connections.set("Connections: 0")
    Label(window, textvariable=L_connections).pack()
    bg_label = Label(window)
    bg_image = Image.open("background.png")
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label.config(image=bg_photo)
    bg_label.pack()
    window.update()
    f = open("serverConfig.json")
    data = json.load(f)
    host = data["host"]
    port = data["port"]
    f.close()
    window.protocol("WM_DELETE_WINDOW",onClosing)
    Button(parent, text="Zaključaj sve", command=lambda: restart()).pack(padx=5)
    labels = {}
    while True:
        global factory
        cons = factory.connections
        
        for key in [k for k in cons.keys() if k not in labels]:
            print(key)
            labels[key] = Label(window,text=f"{key} : {cons[key]}")
            labels[key].pack()
        
        for key in [k for k in labels.keys() if k not in cons]:
            labels[key].destroy()
            del labels[key]
        L_connections.set(f"Connections: {len(labels)}")
        window.update()
        time.sleep(0.1)





rfh = logging.handlers.RotatingFileHandler(
    filename='serverLogger.txt',
    mode='a',
    maxBytes=100 * 1024 * 1024,
    backupCount=2,
    encoding="utf-8",
    delay=0
)
logging.basicConfig(handlers=[rfh], level=logging.DEBUG,
                    format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')
logger = logging.getLogger("serverLogger")
if __name__ == '__main__':
    t = threading.Thread(target=runLoop,daemon=True).start()
    factory = ChatFactory()
    f = open("serverConfig.json")
    data = json.load(f)
    port = data["port"]       
    f.close()
    reactor.listenTCP(port, factory)
    reactor.run()
