# -*- coding: utf-8 -*-
"""
Created on Sun May 17 23:45:24 2026

@author: ediso
"""

import os
import json
import datetime
import requests
import xml.etree.ElementTree as ET
from urllib.parse import quote
from google import genai
from google.genai import types
from pydantic import BaseModel
import firebase_admin
from firebase_admin import credentials, db

# ==========================================
# 🧬 龍雲的數位抗體結構 (定義 AI 輸出的格式)
# ==========================================
class DigitalAntibody(BaseModel):
    suspicious_headline: str  # 攔截到的可疑標題
    truth_status: str         # 真偽狀態 (例如：真實 / 錯誤 / 缺乏證據)
    fact_check_summary: str   # 拆解後的真相摘要
    confidence_score: int     # 龍雲的判定信心指數 (0-100)

class DailyReport(BaseModel):
    interceptions: list[DigitalAntibody] # 今日攔截清單
    overall_threat_level: str            # 整體網路環境威脅等級

def run():
    print("🤖 龍雲排程啟動：開始巡邏網路汪洋，攔截可疑謠言...")
    
    # 1. 🐉 龍雲的雙棲讀取機制 (連線 Firebase)
    if not firebase_admin._apps:
        if os.path.exists("firebase_key.json"):
            cred = credentials.Certificate("firebase_key.json")
        else:
            firebase_env = os.getenv("FIREBASE_CREDENTIALS")
            if not firebase_env:
                raise ValueError("找不到 Firebase 雲端金鑰記憶！")
            cred_dict = json.loads(firebase_env)
            cred = credentials.Certificate(cred_dict)
            
        # ⚠️ 請務必將下方網址換成你的 Firebase Realtime Database 網址
        firebase_admin.initialize_app(cred, {'databaseURL': "https://longyun-scanner-default-rtdb.firebaseio.com/"})

    # 2. 🛡️ 安全讀取 Gemini API Key (從環境變數)
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("找不到 GEMINI_API_KEY 環境變數！")
    client = genai.Client(api_key=api_key)

    # 3. 溯源觸角：鎖定可疑的網路資訊
    # 改變狩獵目標，專門搜尋可能帶有謠言特徵的新聞或討論
    query = quote("網傳 OR 謠言 OR 瘋傳 OR 詐騙 OR 假消息")
    rss_url = f"https://news.google.com/rss/search?q={query}&hl=zh-TW&gl=TW&ceid=TW:zh-Hant"
    res = requests.get(rss_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
    
    headlines = ""
    root = ET.fromstring(res.text)
    # 抓取前 20 則最新資訊進行掃描
    for item in root.findall('.//item')[:20]:
        title_element = item.find('title')
        if title_element is not None:
            headlines += f"- {title_element.text}\n"

    # 4. 拆解型胃袋：AI 判定真偽與抗體生成
    prompt = f"你現在是名為「龍雲」的網路生態守護者，專門吞噬並拆解網路謠言。請掃描以下20則近期網路上熱傳的標題：\n{headlines}\n請從中挑選出最可疑的3則資訊進行拆解，判斷其真偽，並產出事實查核的「數位抗體」。"
    config = types.GenerateContentConfig(response_mime_type="application/json", response_schema=DailyReport)
    
    print("🧠 啟動拆解型胃袋，正在生成數位抗體...")
    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt, config=config)
    result = json.loads(response.text)

    # 5. 寫入資料庫 (台灣時間)
    TW_TZ = datetime.timezone(datetime.timedelta(hours=8))
    now_tw = datetime.datetime.now(TW_TZ)
    
    # 改變資料庫存放路徑，存入專屬的 rumor_interceptions (謠言攔截區)
    ref = db.reference(f'rumor_interceptions/{now_tw.strftime("%Y-%m-%d")}')
    ref.set(result)
    
    print(f"✅ 成功寫入今日攔截紀錄！龍雲共生成了 {len(result['interceptions'])} 組數位抗體。")

if __name__ == "__main__":
    run()