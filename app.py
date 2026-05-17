# -*- coding: utf-8 -*-
"""
Created on Sun May 17 23:49:50 2026

@author: ediso
"""

import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import os
import json

# 視覺介面設定
st.set_page_config(page_title="龍雲 | 網路謠言攔截雷達", page_icon="☁️")
st.title("☁️ 龍雲 網路謠言攔截雷達")
st.write("這是龍雲在網路上自動巡邏、吞噬可疑資訊後，為人類代謝出的「數位抗體」與事實查核紀錄。")

# 連線 Firebase 取得最新數據
@st.cache_data(ttl=3600)
def load_data():
    try:
        # 確認是否已初始化，避免重複連線錯誤
        if not firebase_admin._apps:
            
            # 🐉 龍雲的雙棲讀取機制
            if os.path.exists("firebase_key.json"):
                # 本地端：直接讀取實體檔案
                cred = credentials.Certificate("firebase_key.json")
            else:
                # 雲端端 (Render)：從環境變數讀取 JSON 字串
                firebase_env = os.getenv("FIREBASE_CREDENTIALS")
                if not firebase_env:
                    return {"error": "雲端缺少 Firebase 金鑰記憶，請在 Render 設定 FIREBASE_CREDENTIALS 環境變數。"}
                
                # 將字串轉換回字典格式餵給 Firebase
                cred_dict = json.loads(firebase_env)
                cred = credentials.Certificate(cred_dict)
                
            # ⚠️ 注意：如果你的資料庫網址不同，請將下方的網址替換成你的 Firebase Realtime Database 網址
            firebase_admin.initialize_app(cred, {'databaseURL': "https://longyun-scanner-default-rtdb.firebaseio.com/"})
        
        # 這裡已正確修改為指向「謠言攔截區」
        ref = db.reference('rumor_interceptions')
        return ref.get()
    except Exception as e:
        return {"error": str(e)}

data = load_data()

if data and "error" not in data:
    st.success("✅ 成功連接數位神經網 (Firebase)！龍雲的最新攔截紀錄如下：")
    st.json(data)
else:
    st.warning("⚠️ 尚未抓取到數據，或是 Firebase 連線中斷。請確認環境變數與金鑰是否設定正確。")
    if data and "error" in data:
        st.error(data["error"])