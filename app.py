# -*- coding: utf-8 -*-
"""
Created on Tue May 19 15:08:17 2026

@author: ediso
"""

import streamlit as st
import pandas as pd
import firebase_admin
from firebase_admin import credentials, db
import os, json

# 初始化 Firebase 連線
@st.cache_resource
def init_firebase():
    if not firebase_admin._apps:
        # 優先讀取環境變數，若無則讀取本機檔案
        if "FIREBASE_CREDENTIALS" in os.environ:
            cred_dict = json.loads(os.environ["FIREBASE_CREDENTIALS"])
            cred = credentials.Certificate(cred_dict)
        else:
            cred = credentials.Certificate("firebase_key.json")
        firebase_admin.initialize_app(cred, {'databaseURL': "https://longyun-scanner-default-rtdb.firebaseio.com/"})

init_firebase()

st.set_page_config(page_title="龍雲 | 戰略儀表板", layout="wide")
st.title("👁️ 龍雲：戰略儀表板 (God's Eye OS)")

# 1. 互動式對話介面 (決策模擬)
with st.expander("💬 與龍雲進行決策模擬 (Scenario Planning)"):
    user_scenario = st.text_input("輸入你想模擬的情境：")
    if st.button("啟動模擬"):
        st.write(f"龍雲正在分析情境：{user_scenario} ...")
        # 這裡未來可串接 Gemini API 進行即時推演

# 2. 歷史回顧側邊欄
st.sidebar.header("控制台")
selected_date = st.sidebar.date_input("回顧日期")

# 3. 讀取數據
@st.cache_data(ttl=600)
def load_data():
    try:
        ref = db.reference('gods_eye_matrix')
        data = ref.get()
        return data
    except Exception as e:
        return {"error": str(e)}

data = load_data()

if data:
    # 根據選擇的日期抓取資料
    date_str = selected_date.strftime("%Y-%m-%d")
    matrix_data = data.get(date_str)
    
    if matrix_data:
        st.subheader(f"📅 數據時間點: {matrix_data.get('timestamp', date_str)}")
        
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📡 1. 黑天鵝雷達", 
            "👁️ 2. 矩陣解碼器", 
            "⚖️ 3. 賽博照妖鏡", 
            "🔮 4. 拉普拉斯預言", 
            "🧬 5. 創世引擎"
        ])
        
        with tab1:
            st.info(f"**預警總結**：{matrix_data['black_swan']['warning_summary']}")
            st.write(f"🦋 {matrix_data['black_swan']['anomaly_1']}")
            st.write(f"🦋 {matrix_data['black_swan']['anomaly_2']}")
            st.write(f"🦋 {matrix_data['black_swan']['anomaly_3']}")

        with tab2:
            st.write(f"**目標**：{matrix_data['matrix_decoder']['target_controversy']}")
            st.warning(f"**操縱戰術**：{matrix_data['matrix_decoder']['psychological_tactic']}")
            st.success(f"**解碼**：{matrix_data['matrix_decoder']['decoding_summary']}")

        with tab3:
            st.metric("偽善指數", f"{matrix_data['cyber_panopticon']['hypocrisy_index']}%")
            st.write(f"過去承諾：{matrix_data['cyber_panopticon']['past_statement']}")
            st.write(f"今日發言：{matrix_data['cyber_panopticon']['current_statement']}")

        with tab4:
            ld = matrix_data['laplace_demon']
            st.progress(ld['probability_1']/100, text=ld['prediction_1'])
            st.progress(ld['probability_2']/100, text=ld['prediction_2'])
            st.progress(ld['probability_3']/100, text=ld['prediction_3'])

        with tab5:
            st.subheader(matrix_data['genesis_engine']['new_product_name'])
            st.write(f"估值：{matrix_data['genesis_engine']['estimated_valuation']}")
            st.info(matrix_data['genesis_engine']['architecture_description'])
            
    else:
        st.warning(f"該日期 {date_str} 尚未有數據記錄。")
else:
    st.error("無法連線至 Firebase 資料庫，請檢查環境變數。")