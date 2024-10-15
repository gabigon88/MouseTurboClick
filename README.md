# MouseTurboClick

用python練習寫連滑鼠連點程式
程式截圖
![image](/out/preview.png)

## 執行方式

<font color=#E60000>win10 64bit</font>的系統下執行<font color=#E60000>MouseTurboClick.exe</font>
此檔案是用pyinstaller打包好的exe檔
但受限於pyinstaller打包的限制，檔案無法在win7使用
另外我電腦的python是64 bit的，理論上打包出來的exe 不能在32bit系統上執行

## 若用指令方式執行

```python
  python GUI.py
```

## 使用說明

要特別提醒一下，本程式觸發滑鼠連點的方式
跟目前網路上可以找到的連點程式都<font color=#E60000>不相同</font>
目前網上幾乎都是由鍵盤觸發(ex. F9開始連點、F10停止連點)
本程式是按下開始連點後，<font color=#E60000>壓住要連發的滑鼠鍵</font>，才會自動連點
(要連點左鍵就壓住左鍵，要連點右鍵就壓住右鍵)

## 檔案架構

GUI.py `-> 主程式(GUI)`
myGlobalHook.py `-> 鍵盤滑鼠 event的listener(是thread)`
mouseTurboClick.py `-> 發出滑鼠連點virtual event的thread`

## UML圖

![image](/out/preview_UML/preview_UML.png)

## 尚可改善

- [X]  增加keyborad event listener，以提供除了點擊UI button外的啟動暫停方式
- [X]  增加滑鼠中鍵連點功能(感覺沒有需求?)
- [ ]  新增模式切換, 能選擇 [滑鼠壓下才連點] 和 [啟動自動連點] 兩種模式
- [ ]  讀寫config檔, 保存使用者習慣

## 後記

當年學完 java後也曾經練習此程式
此程式的功能會用到 1.GUI建置 2.thread使用 3.class間的呼叫
也算是一種自我檢驗的集合練習
專案整體很小但有一點點應用程式設計的架構了

最後，紀錄一下在coding中遇到的困難

1. 要找python的mouse event listener，因為python不像java有內建套件可以處理滑鼠事件。
   這部分上網查就可以查到很多套件了ex. pynput、mouse、pyautogui等等。
   我一開始選用pyautogui，結果寫到一半發現，套件只能發出virtual mouse event，不能監聽，所以套件換成使用pynput。
2. mouse event listener也會監聽到自己發出的virtual mouse event......。
   一開始我是寫成滑鼠press時 flag=true，release時 flag=false，當flag為true時 持續連點
   但執行後一直不如預期，找不出問題在哪，後來去看官方文件，才知道程式發出的虛擬事件也會監聽到。
   解析流程如下：
   實體左鍵壓下→監聽者發現左鍵壓下→開始連點→虛擬左鍵壓下→虛擬左鍵鬆開→監聽者發現左鍵鬆開→停止連點
   (但此時實體左鍵還是壓著的)
   這部分debug超久的，會重新用python寫滑鼠連點，有一個原因也是以前用 java寫的原始碼自己都沒有保存下來，所以也沒辦法看以前怎麼解決的，最後是靈機一動想到，每次滑鼠press與release都將flag反轉一次就可以解決了。

## 2024後記

最近有點時間 來把當初的大坑給補上，史詩級調整了不少地方，多年過去了 現在回頭來看當初的code
發現自己好多地方都寫的好青澀

1. listener 本身就是一個thread，建立後可以直接使用，我當年居然還在外面自己包了一層thread
2. 雖然我有讓視窗關閉時 自動清除thread，但有時候連點thread就是沒正確清除，我這次也把執行序設為daemon，再加一層保障
3. 當初沒加 啟動/停止的hotkey 功能，一方面是我懶 一方面是我也不太有底要怎麼寫
   現在有GPT幫助，一下就加好功能了，也覺得充滿感慨，世界不停地變化，不時俱進的人終將被時代淘汰
