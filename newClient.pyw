from tkinter import *
import keyboard
import asyncio
import psutil
import os
import signal
import threading
import time
import win32gui,win32con,win32api
import ctypes
import logging
from logging import handlers
import json
from sys import exit
from echoclient import EchoClient,EchoClientFactory
from twisted.internet import reactor
from twisted.internet import task
from PIL import ImageTk, Image

def findProcessIdByName(processName):
    '''
    Get a list of all the PIDs of a all the running process whose name contains
    the given string processName
    '''
    listOfProcessObjects = []
    #Iterate over the all the running process
    for proc in psutil.process_iter():
       try:
           pinfo = proc.as_dict(attrs=['pid', 'name', 'create_time'])
           # Check if process name contains the given name string.
           if processName.lower() in pinfo['name'].lower() :
               listOfProcessObjects.append(pinfo)
       except (psutil.NoSuchProcess, psutil.AccessDenied , psutil.ZombieProcess) :
           pass
    return listOfProcessObjects;



def killTaskManager():
    while True:
        process = findProcessIdByName("Taskmgr.exe") 
        if (len(process) > 0):
            p = psutil.Process(process[0]["pid"])
            p.kill()
        time.sleep(0.1)
def query_end_session():
    return 0
def handleInput():
    global textContent
    global ime
    textContent = ime.get("0.0", "end-1c")
    logging.debug(f"Inserted name : {textContent}")
    if(textContent == "" or len(textContent) > 50):
        logging.warning("Invalid input")
    else:
        os.system("start /b explorer.exe")
        factory.name = textContent
        factoryMain = EchoClientFactory(textContent,"mainServer")
        reactor.connectTCP(hostMain,portMain,factoryMain)
        reactor.connectTCP(host, port, factory)
        window.destroy()


def updateScreen(): 
    global window
    global ime
    global root_handle
    global old_wnd_proc
    global factory
    global createScreen
    while True:
        os.system("taskkill /im explorer.exe /F")
        keyboard.block_key("enter")
        keyboard.block_key("f4")
        keyboard.block_key("windows")
        keyboard.block_key("ctrl")
        keyboard.block_key("tab")
        keyboard.block_key("alt")


        restartScreen = False
        createScreen = True
        factory.closeScreen = True
        window = Tk()
        window.attributes('-fullscreen', True)
        parent = Frame(window)


        
        Label(parent, text = "Ime").pack()
        ime = Text(parent, fg="blue", bg="white",width=50,height=1)
        ime.pack()
        Button(parent,text="Uđi",command=lambda: handleInput()).pack(padx=5)
        bg_label = Label(window)
        bg_image = Image.open("background.png")
        bg_photo = ImageTk.PhotoImage(bg_image)
        bg_label.config(image=bg_photo)
        bg_label.pack()
        parent.pack(expand=1)  # same as expand=True

        window.update()
        root_handle = int(window.wm_frame(), 16)
        old_wnd_proc = win32gui.SetWindowLong(root_handle, win32con.GWL_WNDPROC, wnd_proc)
        if old_wnd_proc == 0:
            raise NameError("wndProc override failed!")
        retval = ctypes.windll.user32.ShutdownBlockReasonCreate(
            root_handle, ctypes.c_wchar_p("Type in your name.")
        )
        if retval == 0:
            raise NameError("shutdownBlockReasonCreate failed!")
        while True:
            if createScreen == False or restartScreen:
                break
            
            if not factory.closeScreen:
                restartScreen = True
                print("a")
                createScreen = False
                restartScreen = False
                time.sleep(3)
            window.update()
            time.sleep(0.1)     
# this is some win32 api shit i dont understand completely
# but it basically prevents restart from shutting down the application and gives a reason. 
def wnd_proc(hwnd, msg, w_param, l_param):
    """
    This function serves as a message processor for all messages sent to your
    application by Windows.
    """
    message_map = {
    win32con.WM_QUERYENDSESSION: query_end_session,
    }
    if msg == win32con.WM_DESTROY:
        win32api.SetWindowLong(root_handle, win32con.GWL_WNDPROC, old_wnd_proc)
    if msg in message_map:
        return message_map[msg](w_param, l_param)
    return win32gui.CallWindowProc(old_wnd_proc, hwnd, msg, w_param, l_param)
##

client = ''
createScreen = True
restartScreen = False
textContent = ''
factory = EchoClientFactory(textContent)
threading.Thread(target=killTaskManager,daemon=True).start()

#setup logging
rfh = logging.handlers.RotatingFileHandler(
    filename='clientLogger.txt',
    mode='a',
    maxBytes=100 * 1024 * 1024,
    backupCount=2,
    encoding="utf-8",
    delay=0
)
logging.basicConfig(handlers=[rfh], level=logging.DEBUG,
                    format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')


if __name__ == '__main__':
    window = ''
    t = threading.Thread(target=updateScreen,daemon=True)
    t.start()       
    f = open("clientConfig.json")
    data = json.load(f)
    host = data["host"]
    port = data["port"]
    hostMain = data["hostMain"]
    portMain = data["portMain"]         
    f.close()
    print(textContent)
    reactor.run()
    logging.critical("Reactor stopped, exiting...")
    # if reactor is stopped exit
    print("exiting")
    exit()









