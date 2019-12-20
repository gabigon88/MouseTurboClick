#!/usr/bin/python3

import threading
import gc
import tkinter as tk
import globalMouseHook
import mouseTurboClick 

# 關閉視窗時先清除thread
def close_window():
    stop_click()
    window.destroy()

# 為Scale定義觸發函式
def print_speed(v):
    speedScale.config(label='連點間隔調整: ' + v + '(ms)')

# 取得滑鼠連點的設定值
def get_turbo_status():
    status = []
    if isLeftOn.get():
        status.append('左鍵')
    if isRightOn.get():
        status.append('右鍵')
    status.append('間隔' + str(speedScaleVal.get()) + '(ms)')
    return ' '.join(status)

# 定義啟動連點的函式
def start_click():
    global thread
    if thread is None:
        # 建立一個滑鼠連點的子thread
        thread = mouseTurboClick.mouseTurboClick(mouseHook, speedScaleVal.get()/1000, isLeftOn.get(), isRightOn.get())
        thread.start() # 執行該子thread
    else:
        # 更變目前滑鼠連點的屬性
        thread.set_attributes(speedScaleVal.get()/1000, isLeftOn.get(), isRightOn.get())
    status_label.config(text='啟動中: ' + get_turbo_status())

# 為定義停止連點的函式
def stop_click():
    global thread
    if thread is not None:
        thread.stop()
        thread = None
        gc.collect() # 手動釋放memory
        status_label.config(text='未啟動')

# 追蹤滑鼠postion與event的listener(本身是一個thread)
mouseHook = globalMouseHook.globalMouseHook()
mouseHook.start()

# 用來執行滑鼠連點的thread
thread = None

# 建立UI windows
window = tk.Tk()
window.title('Mouse Turbo Click')
window.geometry('400x250')
window.minsize(400, 250)
window.configure(background='#cccccc')
window.protocol("WM_DELETE_WINDOW", close_window)

# UI標頭
header_label = tk.Label(window, text='滑鼠連點程式', font=('Microsoft JhengHei', 14), pady=5)
header_label.pack()

# UI 連點設定區域
mouseBtn_frame = tk.Frame(window)
mouseBtn_frame.pack(side=tk.TOP)
# UI 左鍵設定區域
isLeftOn = tk.BooleanVar()
leftBtn_checkBtn = tk.Checkbutton(mouseBtn_frame, text='左鍵連點', font=('Microsoft JhengHei', 14), variable=isLeftOn, relief=tk.GROOVE)
leftBtn_checkBtn.select() # 預設勾選左點連點
leftBtn_checkBtn.pack(side=tk.LEFT, padx=3)
# UI 右鍵設定區域
isRightOn = tk.BooleanVar()
rightBtn_checkBtn = tk.Checkbutton(mouseBtn_frame, text='右鍵連點', font=('Microsoft JhengHei', 14), variable=isRightOn, relief=tk.GROOVE)
rightBtn_checkBtn.pack(side=tk.LEFT, padx=3)

# UI 速度設定區域
speed_frame = tk.Frame(window)
speed_frame.pack(side=tk.TOP)
speedScaleVal = tk.IntVar()
# 建立一個尺度滑條，長度320字元，從0開始1000結束，以200為刻度，間距精度為10
speedScale = tk.Scale(speed_frame, font=('Microsoft JhengHei', 13), from_=0, to=1000, variable=speedScaleVal, orient=tk.HORIZONTAL, length=300, showvalue=False, tickinterval=200, resolution=10, command=print_speed)
speedScale.set(100) # 預設間隔為100ms
speedScale.pack()

# UI 啟動停止按鈕區域
button_frame = tk.Frame(window)
button_frame.pack(side=tk.TOP)
startBtn = tk.Button(button_frame, text='開始連點', font=('Microsoft JhengHei', 14), command=start_click)
startBtn.pack(side=tk.LEFT, padx=3)
stopBtn = tk.Button(button_frame, text='停止連點', font=('Microsoft JhengHei', 14), command=stop_click)
stopBtn.pack(side=tk.RIGHT, padx=3)

# UI 狀態顯示區域
status_label = tk.Label(window, text='未啟動', font=('Microsoft JhengHei', 14))
status_label.pack()

window.mainloop()