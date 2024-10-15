import threading
from myGlobalHook import globalMouseHook
from time import sleep
from pynput.mouse import Button, Controller

class mouseTurboClick(threading.Thread):
    def __init__(self, mouseHook: globalMouseHook, interval=0.1, isLeftOn=False, isRightOn=False, isMiddleOn=False):
        threading.Thread.__init__(self, daemon=True) # 設為守護執行緒，當主程序結束後，子執行緒會自動停止
        self.mouseHook = mouseHook
        self.mouse = Controller()
        self.set_attributes(interval, isLeftOn, isRightOn, isMiddleOn)
        self.isRun = True # 用來動態停止無限回圈的flag

    def set_attributes(self, interval, isLeftOn, isRightOn, isMiddleOn):
        self.interval = interval # 設定連點間距
        if interval < 0.01: # 避免間距為0
            self.interval = 0.01
        self.isLeftOn = isLeftOn # 左鍵連點是否開啟
        self.isRightOn = isRightOn # 右鍵連點是否開啟
        self.isMiddleOn = isMiddleOn # 中鍵連點是否開啟

    def run(self):
        while self.isRun:
            if (self.isLeftOn and self.mouseHook.is_leftDown()):
                self.mouse.click(Button.left)
            if (self.isRightOn and self.mouseHook.is_rightDown()):
                self.mouse.click(Button.right)
            if (self.isMiddleOn and self.mouseHook.is_middleDown()):
                self.mouse.click(Button.middle)
            sleep(self.interval)
    
    def stop(self):
        self.isRun = False