# -*- coding: utf-8 -*-
"""
Created on Tue May 19 18:51:52 2026

@author: ediso
"""

import streamlit as st
import pandas as pd
import firebase_admin
from firebase_admin import credentials, db
import os, json
from google import genai

# ==========================================
# 初始化 Firebase 與 Gemini 系統
# ==========================================
@st.cache_resource
def init_system():
    if not firebase_admin._apps:
        if "FIREBASE_CREDENTIALS" in os.environ:
            cred_dict = json.loads(os.environ["FIREBASE_CREDENTIALS"])
            cred = credentials.Certificate(cred_dict)
        else:
            cred = credentials.Certificate("firebase_key.json")
            
        # ⚠️ 注意：請務必將下方的網址替換成你真實的 Firebase 資料庫網址
        firebase_admin.initialize_app(cred, {'databaseURL': "https://longyun-scanner-default-rtdb.firebaseio.com/"})
    
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        return genai.Client(api_key=api_key)
    else:
        return None

client = init_system()

# ==========================================
# 視覺看板介面設定
# ==========================================
st.set_page_config(page_title="龍雲 | 戰略儀表板", layout="wide")
st.title("👁️ 龍雲：戰略儀表板 (God's Eye OS)")

# 1. 互動式對話介面
with st.expander("💬 與龍雲進行決策模擬 (Scenario Planning)"):
    user_scenario = st.text_input("輸入你想模擬的情境：")
    if st.button("啟動模擬"):
        if user_scenario:
            if client:
                with st.spinner("龍雲大腦正在進行多維度推演..."):
                    prompt = f"你現在是龍雲AI全知矩陣，擁有上帝視角。請針對以下情境進行嚴謹的推演與分析：{user_scenario}"
                    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
                    st.markdown(f"**龍雲推演結果**：\n{response.text}")
            else:
                st.error("⚠️ 找不到 GEMINI_API_KEY 環境變數，無法啟動大腦進行推演！")
        else:
            st.warning("請先輸入一個情境！")

# 2. 歷史回顧側邊欄
st.sidebar.header("控制台")
selected_date = st.sidebar.date_input("回顧日期")

# 3. 讀取 Firebase 數據
@st.cache_data(ttl=600)
def load_data():
    try:
        ref = db.reference('gods_eye_matrix')
        return ref.get()
    except Exception as e:
        return {"error": str(e)}

data = load_data()

# ==========================================
# 全知矩陣數據呈現
# ==========================================
if data and isinstance(data, dict):
    
    st.subheader("📈 歷史趨勢與預測軌跡")
    history_records = []
    
    for date_key, matrix in data.items():
        if isinstance(matrix, dict) and 'cyber_panopticon' in matrix and 'laplace_demon' in matrix:
            history_records.append({
                "Date": date_key,
                "偽善指數 (Hypocrisy Index)": matrix['cyber_panopticon'].get('hypocrisy_index', 0),
                "黑天鵝爆發機率 (Black Swan Prob.)": matrix['laplace_demon'].get('probability_1', 0)
            })
            
    if history_records:
        df_history = pd.DataFrame(history_records)
        df_history['Date'] = pd.to_datetime(df_history['Date'])
        df_history = df_history.set_index('Date')
        st.line_chart(df_history, color=["#FF4B4B", "#00FFCC"])
    else:
        st.info("⚠️ 目前尚無足夠的歷史數據可繪製趨勢圖。")
        
    st.divider()
    
    date_str = selected_date.strftime("%Y-%m-%d")
    matrix_data = data.get(date_str)
    
    if matrix_data:
        st.success(f"已成功載入 {date_str} 的全知矩陣數據")
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

            # 🌍 新增：動態繪製全球異動定位圖
            if 'anomaly_1_lat' in matrix_data['black_swan']:
                st.subheader("🌍 全球異動定位圖")
                map_df = pd.DataFrame({
                    'lat': [matrix_data['black_swan']['anomaly_1_lat'], 
                            matrix_data['black_swan']['anomaly_2_lat'], 
                            matrix_data['black_swan']['anomaly_3_lat']],
                    'lon': [matrix_data['black_swan']['anomaly_1_lon'], 
                            matrix_data['black_swan']['anomaly_2_lon'], 
                            matrix_data['black_swan']['anomaly_3_lon']]
                })
                st.map(map_df)

        with tab2:
            st.write(f"**目標事件**：{matrix_data['matrix_decoder']['target_controversy']}")
            st.warning(f"**心理操縱戰術**：{matrix_data['matrix_decoder']['psychological_tactic']}")
            st.success(f"**龍雲解碼結論**：{matrix_data['matrix_decoder']['decoding_summary']}")

        with tab3:
            st.metric("血色偽善指數", f"{matrix_data['cyber_panopticon']['hypocrisy_index']}%")
            st.write(f"**過去承諾**：{matrix_data['cyber_panopticon']['past_statement']}")
            st.error(f"**今日發言**：{matrix_data['cyber_panopticon']['current_statement']}")

        with tab4:
            ld = matrix_data['laplace_demon']
            st.write(f"**預言機總結**：{ld['oracle_summary']}")
            st.progress(ld['probability_1']/100, text=f"{ld['probability_1']}% - {ld['prediction_1']}")
            st.progress(ld['probability_2']/100, text=f"{ld['probability_2']}% - {ld['prediction_2']}")
            st.progress(ld['probability_3']/100, text=f"{ld['probability_3']}% - {ld['prediction_3']}")

        with tab5:
            st.subheader(matrix_data['genesis_engine']['new_product_name'])
            st.metric("華爾街預估初始估值", matrix_data['genesis_engine']['estimated_valuation'])
            st.info(f"**產品架構與商業模式**：\n{matrix_data['genesis_engine']['architecture_description']}")
            
    else:
        st.warning(f"該日期 {date_str} 尚未有數據記錄。")
else:
    st.error("無法連線至 Firebase 資料庫，或資料庫目前為空。請先執行 daily_cron.py 讓大腦寫入第一筆資料！")