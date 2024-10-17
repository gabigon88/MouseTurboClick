import threading
from myGlobalHook import globalMouseHook
from time import sleep
from pynput.mouse import Button, Controller

class mouseTurboClick(threading.Thread):
    def __init__(self, mouseHook: globalMouseHook, interval=0.1, isLeftOn=False, isRightOn=False, isMiddleOn=False, autoMode=0):
        threading.Thread.__init__(self, daemon=True) # 設為守護執行緒，當主程序結束後，子執行緒會自動停止
        self.mouseHook = mouseHook
        self.mouse = Controller()
        self.set_attributes(interval, isLeftOn, isRightOn, isMiddleOn, autoMode)
        self.isRun = True # 用來動態停止無限回圈的flag

    def set_attributes(self, interval, isLeftOn, isRightOn, isMiddleOn, autoMode):
        self.interval = interval # 設定連點間距
        if interval < 0.01: # 避免間距為0
            self.interval = 0.01
        self.isLeftOn = isLeftOn # 左鍵連點是否開啟
        self.isRightOn = isRightOn # 右鍵連點是否開啟
        self.isMiddleOn = isMiddleOn # 中鍵連點是否開啟
        self.autoMode = autoMode # 設定連點模式, 0為下壓模式, 1為全自動模式

    def full_auto_mode(self):
        ''' 只要啟動就持續連點, 故稱全動自動模式'''
        while self.isRun:
            if self.isLeftOn:
                self.mouse.click(Button.left)
            if self.isRightOn:
                self.mouse.click(Button.right)
            if self.isMiddleOn:
                self.mouse.click(Button.middle)
            sleep(self.interval)

    def semi_auto_mode(self):
        ''' 鼠鍵要保持下壓才會連點, 故稱半動自動模式'''
        while self.isRun:
            if (self.isLeftOn and self.mouseHook.is_leftDown()):
                self.mouse.click(Button.left)
            if (self.isRightOn and self.mouseHook.is_rightDown()):
                self.mouse.click(Button.right)
            if (self.isMiddleOn and self.mouseHook.is_middleDown()):
                self.mouse.click(Button.middle)
            sleep(self.interval)

    def run(self):
        if self.autoMode is 0:
            self.semi_auto_mode()
        else:
            self.full_auto_mode()
    
    def stop(self):
        self.isRun = False