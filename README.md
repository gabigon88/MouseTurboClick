# MouseTurboClick
用python練習寫連滑鼠連點程式

## 執行方式
在<font color=#E60000>win10 64bit</font>的系統下<font color=#E60000>直接執行MouseTurboClick.exe</font>開啟<>  
此檔案是用pyinstaller打包好的exe檔  
但pyinstaller的使用限制，無法在win7使用  
又打打包時是用的64位元的python，故無法在32位元的OS上使用  

## 若用指令方式執行
```javascript
  python GUI.py
```

## 使用說明



## 檔案架構
GUI.py `-> 主程式(GUI)`  
globalMouseHook.py `-> mouse event的listener(也是一個thread)`  
mouseTurboClick.py `-> 發出滑鼠連點virtual event的thread`   

## UML檔


## 後記
當年在學完 java後也曾經寫過此程式  
此程式的功能會練習到 GUI建置、thread使用和class間的呼叫  
也算是一種自我檢驗的集合練習  
整體架構很小但在coding時至少還有一點點設計的感覺出來了  
也是一個筆者很喜歡的練習(笑)  
  
最後，紀錄一下在coding中遇到的困難  
* 1.要找python的mouse event listener，因為python不像java有內建套件可以處理滑鼠事件。  這部分上網查就可以查到很多套件了ex. pynput、mouse、pyautogui等等。  
筆者一開始選用pyautogui，結果寫到一半發現套件只能發出virtual mouse event，不能監聽，所以只好換成使用pynput套件。  
* 2.mouse event listener也會監聽到自己發出的virtual mouse event......。  
分析一下流程如下：實體左鍵壓下→監聽者發現左鍵壓下→開始連點→虛擬左鍵壓下→虛擬左鍵鬆開→監聽者發現左鍵鬆開→停止連點。  
一開始一直找不出問題在哪，後來去看官方文件，才知道程式發出的虛擬事件也會監聽到。  
這部分筆者搞超久的，會重新用python寫滑鼠連點，有一個原因也是以前用 java寫的原始碼自己都沒有保存下來，所以也沒辦法看以前怎麼解決的，最後是靈機一動想到，每次滑鼠press與release都將flag反轉一次就可以解決了。(原先是設計press時assign成true，release時assign成false)
