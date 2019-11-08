import threading
import gc
import tkinter as tk
import globalMouseHook
import mouseTurboClick

# 追蹤滑鼠postion與event的listener
globalMouseHook = globalMouseHook.globalMouseHook()
globalMouseHook.start()

# 用來執行滑鼠連點的子thread
thread = None

# 建立UI
window = tk.Tk()
window.title('Mouse Turbo Click')
window.geometry('500x300')
window.configure(background='gray')
window.attributes("-topmost", True)

header_label = tk.Label(window, text='滑鼠連點程式', font=('Microsoft JhengHei', 14))
header_label.pack()

leftBtn_frame = tk.Frame(window)
leftBtn_frame.pack(side=tk.TOP)
leftBtn_label = tk.Label(leftBtn_frame, text='左鍵連點', font=('Microsoft JhengHei', 14))
leftBtn_label.pack(side=tk.LEFT)
isLeftOn = tk.BooleanVar()
leftBtn_checkBtn = tk.Checkbutton(leftBtn_frame, variable=isLeftOn)
leftBtn_checkBtn.select() # 預設勾選左點連點
leftBtn_checkBtn.pack(side=tk.LEFT)

rightBtn_frame = tk.Frame(window)
rightBtn_frame.pack(side=tk.TOP)
rightBtn_label = tk.Label(rightBtn_frame, text='右鍵連點', font=('Microsoft JhengHei', 14))
rightBtn_label.pack(side=tk.LEFT)
isRightOn = tk.BooleanVar()
rightBtn_checkBtn = tk.Checkbutton(rightBtn_frame, variable=isRightOn)
rightBtn_checkBtn.pack(side=tk.LEFT)

speed_frame = tk.Frame(window)
speed_frame.pack(side=tk.TOP)

# 為Scale定義觸發函式功能
def print_speed(v):
    speedScale.config(label='連點間距調整: ' + v + '(ms)')

speedScaleVal = tk.IntVar()
# 建立一個尺度滑條，長度300字元，從0開始1000結束，以200為刻度，間距精度為10
speedScale = tk.Scale(speed_frame, label='連點間距調整: 0(ms)', font=('Microsoft JhengHei', 12), from_=0, to=1000, variable=speedScaleVal, orient=tk.HORIZONTAL, length=300, showvalue=0, tickinterval=200, resolution=10, command=print_speed)
speedScale.set(100) # 預設間隔為100ms
speedScale.pack()

result_label = tk.Label(window)
result_label.pack()

def startClick():
    global thread
    if (thread == None):
        thread = mouseTurboClick.mouseTurboClick(globalMouseHook, speedScaleVal.get()/1000, isLeftOn.get(), isRightOn.get()) # 建立一個子執行緒
        thread.start() # 執行該子執行緒
        globalMouseHook.setMouseTurboClick(thread)

def stopClick():
    global thread
    if (thread != None):
        thread.stop()
        thread = None
        globalMouseHook.setMouseTurboClick(thread)
        gc.collect() # 手動釋放memory

startBtn = tk.Button(window, text='開始連點', font=('Microsoft JhengHei', 14), command=startClick)
startBtn.pack()
stopBtn = tk.Button(window, text='停止連點', font=('Microsoft JhengHei', 14), command=stopClick)
stopBtn.pack()

window.mainloop()