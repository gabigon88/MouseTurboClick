#!/usr/bin/python3

import tkinter as tk
import myGlobalHook
from mouseTurboClick import mouseTurboClick

class AutoClickerGUI:
    def __init__(self, root: tk):
        self.root = root
        self.root.title('Mouse Turbo Click')
        self.root.geometry('350x350')
        self.root.configure(background='#cccccc')
        self.root.config(padx=20, pady=5)
        self.root.protocol("WM_DELETE_WINDOW", self.close_window)
        
        # 追蹤滑鼠postion與event的listener(本身是一個thread)
        self.mouseHook = myGlobalHook.globalMouseHook()
        # 追蹤鍵盤event的listener(本身是一個thread)
        self.keyboardHook = myGlobalHook.globalKeyboardHook()
        # 用來執行滑鼠連點的thread
        self.click_thread = None

        # 設置grid每一行和每一列都可以伸縮
        for i in range(2):
            self.root.grid_columnconfigure(i, weight=1)
        for i in range(9):
            self.root.grid_rowconfigure(i, weight=1)

        # UI 標頭
        self.header_label = tk.Label(text='滑鼠連點程式', font=('Microsoft JhengHei', 14))
        self.header_label.grid(row=0, column=0, columnspan=2, pady=10, sticky="nsew")

        # UI 連點設定區塊
        self.mouseBtn_frame = tk.Frame(self.root)
        self.mouseBtn_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")
        for i in range(3):
            self.mouseBtn_frame.grid_columnconfigure(i, weight=1)
        # UI 左鍵啟用設定
        self.leftBtn_frame = tk.Frame(self.mouseBtn_frame)
        self.leftBtn_frame.grid(row=0, column=0, sticky="nsew")
        self.isLeftOn = tk.BooleanVar()
        self.leftBtn_checkBtn = tk.Checkbutton(self.leftBtn_frame, text='左鍵連點', font=('Microsoft JhengHei', 14), variable=self.isLeftOn)
        self.leftBtn_checkBtn.select() # 預設勾選左點連點
        self.leftBtn_checkBtn.pack()
        # UI 中鍵啟用設定
        self.middleBtn_frame = tk.Frame(self.mouseBtn_frame)
        self.middleBtn_frame.grid(row=0, column=1, sticky="nsew")
        self.isMiddleOn = tk.BooleanVar()
        self.middleBtn_checkBtn = tk.Checkbutton(self.middleBtn_frame, text='中鍵連點', font=('Microsoft JhengHei', 14), variable=self.isMiddleOn)
        self.middleBtn_checkBtn.pack()
        # UI 右鍵啟用設定
        self.rightBtn_frame = tk.Frame(self.mouseBtn_frame)
        self.rightBtn_frame.grid(row=0, column=2, sticky="nsew")
        self.isRightOn = tk.BooleanVar()
        self.rightBtn_checkBtn = tk.Checkbutton(self.rightBtn_frame, text='右鍵連點', font=('Microsoft JhengHei', 14), variable=self.isRightOn)
        self.rightBtn_checkBtn.pack()

        # UI 連點速度設定
        self.speedScaleVal = tk.IntVar()
        # 建立一個尺度滑條，從0開始1000結束，以200為刻度，間距精度為10
        self.speedScale = tk.Scale(self.root, font=('Microsoft JhengHei', 13), from_=0, to=1000, 
                            variable=self.speedScaleVal, orient=tk.HORIZONTAL, 
                            showvalue=False, tickinterval=200, resolution=10, command=self.print_speed)
        self.speedScale.set(100) # 預設速度為100ms
        self.speedScale.grid(row=2, column=0, columnspan=2, sticky="nsew")

        # UI 熱鍵設定區塊
        self.hotKey_frame = tk.Frame(root)
        self.hotKey_frame.grid(row=4, columnspan=2, sticky="nsew")
        self.isHotKeyOn = tk.BooleanVar()
        self.HotKeyOn_checkBtn = tk.Checkbutton(self.hotKey_frame, text='使用鍵盤快速鍵 啟動/停止', font=('Microsoft JhengHei', 14), variable=self.isHotKeyOn, command=self.on_hotkey_checkBtn_change)
        self.HotKeyOn_checkBtn.select() # 預設勾選使用鍵盤快速鍵
        self.HotKeyOn_checkBtn.pack()

        # 選單標籤
        self.hotkey_label1 = tk.Label(self.root, text="啟動熱鍵")
        self.hotkey_label1.grid(row=5, column=0, sticky="nsew")
        self.hotkey_label2 = tk.Label(self.root, text="停止熱鍵")
        self.hotkey_label2.grid(row=5, column=1, sticky="nsew")

        # 熱鍵選項 F1 到 F12 的list
        self.function_keys = [f"F{i}" for i in range(1, 13)]
        # 第一個下拉選單（啟動自動連點的熱鍵）
        self.selected_start_key = tk.StringVar(value=self.function_keys[8]) #預設F9啟動
        self.start_key_menu = tk.OptionMenu(self.root, self.selected_start_key, *self.function_keys)
        self.start_key_menu.grid(row=6, column=0, sticky="nsew")
        self.selected_start_key.trace_add("write", self.set_hotkeys)
        # 第二個下拉選單（停止自動連點的熱鍵）
        self.selected_stop_key = tk.StringVar(value=self.function_keys[9]) #預設F10停止
        self.stop_key_menu = tk.OptionMenu(self.root, self.selected_stop_key, *self.function_keys)
        self.stop_key_menu.grid(row=6, column=1, sticky="nsew")
        self.selected_stop_key.trace_add("write", self.set_hotkeys)

        # UI 啟動/停止按鈕
        self.startBtn = tk.Button(self.root, text='開始連點', font=('Microsoft JhengHei', 14), command=self.start_click)
        self.startBtn.grid(row=7, column=0, pady=5, sticky="nsew")
        self.stopBtn = tk.Button(self.root, text='停止連點', font=('Microsoft JhengHei', 14), command=self.stop_click)
        self.stopBtn.grid(row=7, column=1, pady=5, sticky="nsew")

        # UI 啟動狀態顯示
        self.status_label = tk.Label(self.root, text='未啟動', font=('Microsoft JhengHei', 14))
        self.status_label.grid(row=8, column=0, columnspan=2, sticky="nsew")

        self.set_hotkeys()

    # 關閉視窗時先清除thread
    def close_window(self):
        self.stop_click()
        self.mouseHook.stop()
        self.keyboardHook.stop()
        self.root.destroy()

    # Scale觸發函式
    def print_speed(self, v):
        self.speedScale.config(label='連點間隔調整: ' + v + '(ms)')

    # 取得設定值資訊
    def get_turbo_status(self):
        status = []
        if self.isLeftOn.get():
            status.append('左鍵')
        if self.isRightOn.get():
            status.append('右鍵')
        if self.isMiddleOn.get():
            status.append('中鍵')
        status.append('間隔' + str(self.speedScaleVal.get()) + '(ms)')
        return ' '.join(status)

    # 啟動連點
    def start_click(self):
        if self.click_thread is None:
            self.click_thread = mouseTurboClick(self.mouseHook, self.speedScaleVal.get()/1000, 
                                    self.isLeftOn.get(), self.isRightOn.get(), self.isMiddleOn.get())
            self.click_thread.start()
        else:
            self.click_thread.set_attributes(self.speedScaleVal.get()/1000, 
                                    self.isLeftOn.get(), self.isRightOn.get(), self.isMiddleOn.get())
        self.status_label.config(text='啟動中: ' + self.get_turbo_status())

    # 停止連點
    def stop_click(self):
        if self.click_thread is None:
            return
        self.click_thread.stop()
        self.status_label.config(text='未啟動')
    
    # 設定快速鍵
    def set_hotkeys(self, *arg):
        self.keyboardHook.clear_hotkey() # 登記熱鍵前, 先清除以前的熱鍵
        self.keyboardHook.set_hotKey(self.selected_start_key.get(), self.start_click)
        self.keyboardHook.set_hotKey(self.selected_stop_key.get(), self.stop_click)

    # 啟用快速鍵的checkbox狀態改變時
    def on_hotkey_checkBtn_change(self):
        if self.isHotKeyOn.get():
            self.set_hotkeys()
        else:
            self.keyboardHook.clear_hotkey()
    
# 啟動Tkinter應用
root = tk.Tk()
app = AutoClickerGUI(root)
root.mainloop()
