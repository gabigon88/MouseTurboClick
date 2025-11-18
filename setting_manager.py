import os
import json

class SettingManager:
    def __init__(self, filename="settings.ini"):
        # 取得目前 py 檔所在的資料夾路徑
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.file_path = os.path.join(self.base_path, filename)

        # 預設設定值
        self.default_settings = {
            "window_position": "350x400+800+400",
            "isLeftOn": True,
            "isMiddleOn": False,
            "isRightOn": False,
            "speed": 100,
            "isHotKeyOn": True,
            "hotkey_start": "F9",
            "hotkey_stop": "F10",
            "mode": 0,
        }

        # 設定內容（讀檔後會覆蓋）
        self.settings = {}

        self.load()  # 初始化時自動讀檔

    def load(self):
        """讀取設定檔，若不存在則建立預設檔案"""
        if not os.path.exists(self.file_path):
            self.settings = self.default_settings.copy()
            self.save()  # 自動建立新檔案
            return

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content == "":
                    # 空檔案 → 使用預設設定
                    self.settings = self.default_settings.copy()
                else:
                    self.settings = json.loads(content)
        except Exception:
            # 檔案損壞或格式錯誤 → 建立預設設定
            self.settings = self.default_settings.copy()
            self.save()

    def save(self):
        """將設定內容寫回檔案"""
        with open(self.file_path, "w", encoding="utf-8") as f:
            f.write(json.dumps(self.settings, indent=4, ensure_ascii=False))

    def get(self, key, default=None):
        """取得設定值"""
        return self.settings.get(key, default)

    def set(self, key, value):
        """設定值並自動儲存"""
        self.settings[key] = value
        self.save()

    def reset_all(self):
        """設定檔全部恢復預設值"""
        self.settings = self.default_settings.copy()
        self.save()