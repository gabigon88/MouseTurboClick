import threading
import gc
import tkinter as tk
import globalMouseHook

thread = None

window = tk.Tk()
window.title('Mouse Turbo Click')
window.geometry('500x300')
window.configure(background='gray')

def printSelf():
    result_label.configure(text=isLeftBtn.get())

header_label = tk.Label(window, text='滑鼠連點程式', font=('Arial', 14))
header_label.pack()

leftBtn_frame = tk.Frame(window)
leftBtn_frame.pack(side=tk.TOP)
leftBtn_label = tk.Label(leftBtn_frame, text='左鍵連點', font=('Arial', 14))
leftBtn_label.pack(side=tk.LEFT)
isLeftBtn = tk.BooleanVar()
leftBtn_checkBtn = tk.Checkbutton(leftBtn_frame, variable=isLeftBtn)
leftBtn_checkBtn.select() # 預設勾選左點連點
leftBtn_checkBtn.pack(side=tk.LEFT)

rightBtn_frame = tk.Frame(window)
rightBtn_frame.pack(side=tk.TOP)
rightBtn_label = tk.Label(rightBtn_frame, text='右鍵連點', font=('Arial', 14))
rightBtn_label.pack(side=tk.LEFT)
isRightBtn = tk.BooleanVar()
rightBtn_checkBtn = tk.Checkbutton(rightBtn_frame, variable=isRightBtn)
rightBtn_checkBtn.pack(side=tk.LEFT)

speed_frame = tk.Frame(window)
speed_frame.pack(side=tk.TOP)

# 定義一個觸發函式功能
def print_speed(v):
    speedScale.config(label='連點間距調整: ' + v + '(ms)')

speedScaleVal = tk.IntVar()
# 建立一個尺度滑條，長度300字元，從0開始1000結束，以200為刻度，間距精度為10
speedScale = tk.Scale(speed_frame, label='連點間距調整: 0(ms)', font=('Arial', 12), from_=0, to=1000, variable=speedScaleVal, orient=tk.HORIZONTAL, length=300, showvalue=0, tickinterval=200, resolution=10, command=print_speed)
speedScale.set(100) # 預設間隔為100ms
speedScale.pack()

result_label = tk.Label(window)
result_label.pack()

def startClick():
    global thread
    if (thread == None):
        thread = globalMouseHook.globalMouseHook(isLeftBtn.get(), isRightBtn.get(), (speedScaleVal.get()/1000)) # 建立一個子執行緒
        thread.start() # 執行該子執行緒

def stopClick():
    global thread
    if (thread != None):
        thread.stop()
        thread = None
        gc.collect() # 手動釋放memory

calculate_btn = tk.Button(window, text='開始連點', font=('Arial', 14), command=startClick)
calculate_btn.pack()
calculate_btn = tk.Button(window, text='停止連點', font=('Arial', 14), command=stopClick)
calculate_btn.pack()

window.mainloop()