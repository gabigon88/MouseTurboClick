# MouseTurboClick

用python練習寫連滑鼠連點程式  
程式截圖  
![image](/out/preview.png)  

## 執行方式

win10 64bit 直接執行 MouseTurboClick.exe  
此檔案是用pyinstaller打包的exe檔  
但受限於pyinstaller限制，檔案無法在win7使用  
另外我電腦python是64 bit的，理論上打包出來的exe 不能在32bit系統上執行  

## 若用指令方式執行

```python
  python GUI.py
```

## 使用說明

本程式有兩種模式，觸發連點的方式不同  
1. 鼠鍵下壓模式: 連點啟動後，只有壓住滑鼠鍵時，才會自動連點  
ex. 要連點左鍵就壓住左鍵，要連點右鍵就壓住右鍵  
2. 全自動模式: 與網上找到的連點程式相同，由鍵盤觸發  
ex. 鍵盤按下F9後，會開始自動連點，直到鍵盤按下F10才會停止  

另外補充，我有發現code在macOS上，下壓模式 會無法如期運行，這部份我應該不會處理  

## 檔案架構

GUI.py `-> 主程式(GUI)`  
myGlobalHook.py `-> 鍵盤滑鼠event 的listener(是thread)`  
mouseTurboClick.py `-> 滑鼠連點 發出virtual event的thread`  

## UML圖

![image](/out/preview_UML/preview_UML.png)

## 尚可改善

- [X]  增加keyborad event listener，以提供除了點擊UI button外的啟動暫停方式
- [X]  增加滑鼠中鍵連點功能 (感覺沒有需求?)
- [X]  新增模式切換, 能選擇 [滑鼠壓下才連點] 和 [啟動自動連點] 兩種模式
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
2. mouse event listener也會監聽到自己發出的virtual mouse event......  
   一開始我是寫成滑鼠press時 flag=true，release時 flag=false，當flag為true時 持續連點  
   但執行後一直不如預期，找不出問題在哪，後來去看官方文件，才知道程式發出的虛擬事件也會監聽到。  
   解析流程如下：  
   實體左鍵壓下→監聽者發現左鍵壓下→開始連點→虛擬左鍵壓下→虛擬左鍵鬆開→監聽者發現左鍵鬆開→停止連點  
   (但此時實體左鍵還是壓著的)  
   這部分debug超久的，會重新用python寫滑鼠連點，一方面也是 以前用java寫的原始碼自己都沒有保存下來  
   所以沒辦法看以前怎麼解決的，最後是靈機一動想到，每次滑鼠press與release都將flag反轉一次就可以解決了。  

## 2024後記

最近有點時間，把當初的大坑給補上，史詩級調整了不少地方，多年過去了 現在回頭來看當初的code  
發現自己好多地方都寫的好青澀  

1. listener 本身就是一個thread，建立後可以直接使用，我當年居然還在外面自己包了一層thread
2. 雖然我有讓視窗關閉時 自動清除thread，但有時候連點thread就是沒正確清除  
   我這次把執行序設為daemon，主程序結束後強制停止，再加一層保障
3. 當初沒加 hotkey功能，一方面是我懶，另外是我也知道要怎麼寫，當年我可搞不清楚callback要怎麼用  
   現在有GPT幫助，一下就加好功能了，也覺得充滿感慨，科技進步的速度日新月異
