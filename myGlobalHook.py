from pynput import mouse, keyboard

class globalMouseHook():
    def __init__(self):
        # in a non-blocking fashion
        self.listener = mouse.Listener(
            on_move=self.on_move,
            on_click=self.on_click)
        self.listener.start()
        
        self.isLeftDown = False
        self.isRightDown = False
        self.isMiddleDown = False

    def on_move(self, x, y):
        # print('Pointer at {0}'.format((x, y)))
        return

    def on_click(self, x, y, button, pressed):
        # print('{0} at {1} with {2}'.format('Pressed' if pressed else 'Released', (x, y), button))
        if button == mouse.Button.left:
            self.isLeftDown = not self.isLeftDown
        if button == mouse.Button.right:
            self.isRightDown = not self.isRightDown
        if button == mouse.Button.middle:
            self.isMiddleDown = not self.isMiddleDown
        
    def is_leftDown(self):
        return self.isLeftDown

    def is_rightDown(self):
        return self.isRightDown
    
    def is_middleDown(self):
        return self.isMiddleDown 
    
    def return_default(self):
        self.isLeftDown = False
        self.isRightDown = False
        self.isMiddleDown = False

    def stop(self):
        if self.listener is not None:
            self.listener.stop()

class globalKeyboardHook():
    def __init__(self):
        self.hotkeys = {}  # 用來動態更新熱鍵

        # in a non-blocking fashion:
        self.listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release)
        self.listener.start()

    def clear_hotkey(self):
        self.hotkeys.clear()  # 清除目前的所有熱鍵

    def set_hotKey(self, hotkey_str, callback):
        hotkey = keyboard.HotKey(
            keyboard.HotKey.parse(f'<{hotkey_str}>'), callback)
        self.hotkeys[hotkey_str] = hotkey  # 添加新的熱鍵

    def on_press(self, key):
        for hotkey in self.hotkeys.values():
            hotkey.press(self.listener.canonical(key))

    def on_release(self, key):
        for hotkey in self.hotkeys.values():
            hotkey.release(self.listener.canonical(key))

    def stop(self):
        if self.listener is not None:
            self.listener.stop()