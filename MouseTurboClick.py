import threading
import globalMouseHook
from time import sleep
from pynput.mouse import Button, Controller

class mouseTurboClick(threading.Thread):
    def __init__(self, mouseHook: globalMouseHook, interval=0.1, isLeftOn=False, isRightOn=False):
        threading.Thread.__init__(self)
        self.mouse = Controller()
        self.mouseHook = mouseHook
        if (interval < 0.1): #避免間距為0
            interval = 0.1
        self.interval = interval
        self.isLeftOn = isLeftOn
        self.isRightOn = isRightOn
        self.isRun = True
        self.isLeftDown = False
        self.isRightDown = False

    def run(self):
        while (self.isRun):
            if (self.isLeftOn and self.mouseHook.getIsLeftDown()):
                self.mouse.click(Button.left)
            if (self.isRightOn and self.mouseHook.getIsRightDown()):
                self.mouse.click(Button.right)
            sleep(self.interval)
    
    def stop(self):
        self.isRun = False