import threading
import globalMouseHook
from time import sleep
from pynput.mouse import Button, Controller

class mouseTurboClick(threading.Thread):
    def __init__(self, mouseHook: globalMouseHook, interval=0.1, isLeftOn=False, isRightOn=False):
        threading.Thread.__init__(self)
        self.mouseHook = mouseHook
        self.mouse = Controller()
        self.set_attributes(interval, isLeftOn, isRightOn)
        self.isRun = True # 連點是否執行中

    def set_attributes(self, interval, isLeftOn, isRightOn):
        self.interval = interval # 設定連點間距
        if interval < 0.01: # 避免間距為0
            self.interval = 0.01
        self.isLeftOn = isLeftOn # 左鍵連點是否開啟
        self.isRightOn = isRightOn # 右鍵連點是否開啟

    def run(self):
        while self.isRun:
            if (self.isLeftOn and self.mouseHook.is_leftDown()):
                self.mouse.click(Button.left)
            if (self.isRightOn and self.mouseHook.is_rightDown()):
                self.mouse.click(Button.right)
            sleep(self.interval)
    
    def stop(self):
        self.isRun = False