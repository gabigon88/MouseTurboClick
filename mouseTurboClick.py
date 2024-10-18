import threading
from myGlobalHook import globalMouseHook
from time import sleep
from pynput.mouse import Button, Controller

class mouseTurboClick(threading.Thread):
    def __init__(self, mouseHook: globalMouseHook, interval=0.1, leftOn=False, rightOn=False, middleOn=False, autoMode=0):
        threading.Thread.__init__(self, daemon=True) # 設為守護執行緒，當主程序結束後，子執行緒會自動停止
        self.mouseHook = mouseHook
        self.mouse = Controller()
        self.set_attributes(interval, leftOn, rightOn, middleOn, autoMode)
        self.running = True # 用來動態停止無限回圈的flag

    def set_attributes(self, interval, leftOn, rightOn, middleOn, autoMode):
        self.interval = interval # 設定連點間距
        if interval < 0.01: # 避免間距為0
            self.interval = 0.01
        self.leftOn = leftOn # 左鍵連點是否開啟
        self.rightOn = rightOn # 右鍵連點是否開啟
        self.middleOn = middleOn # 中鍵連點是否開啟
        self.autoMode = autoMode # 設定連點模式, 0為下壓模式, 1為全自動模式

    def full_auto_mode(self):
        ''' 只要啟動就持續連點, 故稱全動自動模式'''
        while self.running:
            if self.leftOn:
                self.mouse.click(Button.left)
            if self.rightOn:
                self.mouse.click(Button.right)
            if self.middleOn:
                self.mouse.click(Button.middle)
            sleep(self.interval)

    def semi_auto_mode(self):
        ''' 鼠鍵要保持下壓才會連點, 故稱半動自動模式'''
        while self.running:
            if (self.leftOn and self.mouseHook.leftPressed):
                self.mouse.click(Button.left)
            if (self.rightOn and self.mouseHook.rightPressed):
                self.mouse.click(Button.right)
            if (self.middleOn and self.mouseHook.middlePressed):
                self.mouse.click(Button.middle)
            sleep(self.interval)

    def run(self):
        while self.mouseHook.pressedEvent:
            sleep(0.5) # 如果thread執行當下, 滑鼠鍵是下壓狀態就sleep, 等待滑鼠鍵鬆開
        
        if self.autoMode == 0:
            self.semi_auto_mode()
        else:
            self.full_auto_mode()
    
    def stop(self):
        self.running = False