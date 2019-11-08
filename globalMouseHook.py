import threading
import mouseTurboClick
from pynput.mouse import Listener, Button

class globalMouseHook(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.isLeftDown = False
        self.isRightDown = False
        self.mouseTurboClick = None

    def on_move(self, x, y):
        # print('Pointer at {0}'.format((x, y)))
        self.x = x
        self.y = y

    def on_click(self, x, y, button, pressed):
        print('{0} at {1} with {2}'.format('Pressed' if pressed else 'Released', (x, y), button))
        if (pressed):
            if (button == Button.left):
                self.mouseTurboClick.isLeftDown = True
            elif (button == Button.right):
                self.mouseTurboClick.isRightDown = True
        else:
            self.mouseTurboClick.isLeftDown = False
            self.mouseTurboClick.isRightDown = False

    def setMouseTurboClick(self, mouseTurboClick: mouseTurboClick):
        self.mouseTurboClick = mouseTurboClick

    def getIsLeftDown(self):
        return self.isLeftDown

    def getIsRightDown(self):
        return self.isRightDown

    def run(self):
        # Collect events until released
        self.listener = Listener(
            on_move=self.on_move,
            on_click=self.on_click)
        self.listener.start()
    
    def stop(self):
        self.listener.stop()


