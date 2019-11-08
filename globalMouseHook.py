import threading
from time import sleep
from pynput.mouse import Button, Controller
from pynput.mouse import Listener

class globalMouseHook(threading.Thread):
    def __init__(self, isLeftBtn=False, isRightBtn=False, interval=0.1):
        threading.Thread.__init__(self)
        self.isLeftBtn = isLeftBtn
        self.isRightBtn = isRightBtn
        self.interval = interval
        self.mouse = Controller()
        self.isLeftBtnGo = False

    def on_move(self, x, y):
        # print('Pointer at {0}'.format(self.mouse.position))
        return

    def on_click(self, x, y, button, pressed):
        # print('{0} at {1}'.format('Pressed' if pressed else 'Released',(x, y)))
        if (pressed and self.isLeftBtn):
            self.isLeftBtnGo = True
            print (self.isLeftBtnGo)
        elif (not pressed and self.isLeftBtn):
            self.isLeftBtnGo = False
            print (self.isLeftBtnGo)

    def run(self):
        # Collect events until released
        self.listener = Listener(
            on_move=self.on_move,
            on_click=self.on_click)
        self.listener.start()
        while (True):
            print ('1')
            if (self.isLeftBtnGo):
                print ('2')
                self.mouse.press(Button.left)
                self.mouse.release(Button.left)
    
    def stop(self):
        self.listener.stop()
        