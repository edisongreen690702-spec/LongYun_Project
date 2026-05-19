# -*- coding: utf-8 -*-
"""
Created on Tue May 19 14:07:56 2026

@author: ediso
"""

import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import os
import json

st.set_page_config(page_title="龍雲 | God's Eye OS", page_icon="👁️", layout="wide")

# 賽博龐克風格標題
st.markdown("<h1 style='text-align: center; color: #00FFCC;'>👁️ 龍雲：全知矩陣 (God's Eye OS)</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #AAAAAA;'>上帝視角已連線 / 每日五維度降維打擊分析系統</p>", unsafe_allow_html=True)
st.divider()

@st.cache_data(ttl=3600)
def load_data():
    try:
        if not firebase_admin._apps:
            if os.path.exists("firebase_key.json"):
                cred = credentials.Certificate("firebase_key.json")
            else:
                firebase_env = os.getenv("FIREBASE_CREDENTIALS")
                if not firebase_env:
                    return {"error": "雲端缺少 Firebase 金鑰記憶。"}
                cred = credentials.Certificate(json.loads(firebase_env))
            # ⚠️ 請替換為你的真實 Firebase 網址
            firebase_admin.initialize_app(cred, {'databaseURL': "https://longyun-scanner-default-rtdb.firebaseio.com/"})
        
        # 讀取全知矩陣的最新一天數據
        ref = db.reference('gods_eye_matrix')
        data = ref.get()
        if data:
            latest_date = sorted(data.keys())[-1]
            return data[latest_date]
        return None
    except Exception as e:
        return {"error": str(e)}

matrix_data = load_data()

if matrix_data and "error" not in matrix_data:
    st.caption(f"⏱️ 最後運算時間: {matrix_data.get('timestamp', '未知')}")
    
    # 建立五個維度的控制面板分頁
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📡 第一維度：黑天鵝雷達", 
        "👁️ 第二維度：矩陣解碼器", 
        "⚖️ 第三維度：賽博照妖鏡", 
        "🔮 第四維度：拉普拉斯預言", 
        "🧬 第五維度：創世引擎"
    ])
    
    # 1. 邊緣感知 (黑天鵝雷達)
    with tab1:
        st.header("📡 尋找底層的微小震動")
        bs = matrix_data['black_swan']
        st.error(f"**高危險預警總結**：\n{bs['warning_summary']}")
        st.info(f"🦋 震動 1：{bs['anomaly_1']}")
        st.info(f"🦋 震動 2：{bs['anomaly_2']}")
        st.info(f"🦋 震動 3：{bs['anomaly_3']}")

    # 2. 解構當下 (矩陣解碼器)
    with tab2:
        st.header("👁️ 逆向工程網路風向")
        md = matrix_data['matrix_decoder']
        st.subheader(f"🎯 目標事件：{md['target_controversy']}")
        col1, col2 = st.columns(2)
        col1.warning(f"**利用的認知偏差**：\n{md['cognitive_bias_used']}")
        col2.warning(f"**心理操縱戰術**：\n{md['psychological_tactic']}")
        st.success(f"**龍雲解碼結論**：\n{md['decoding_summary']}")

    # 3. 審判權威 (賽博照妖鏡)
    with tab3:
        st.header("⚖️ 權威人士的歷史審判")
        cp = matrix_data['cyber_panopticon']
        st.subheader(f"👨‍⚖️ 審判目標：{cp['target_authority']}")
        
        st.metric(label="血色偽善指數 (0-100)", value=f"{cp['hypocrisy_index']}%", delta="高度警戒" if cp['hypocrisy_index'] > 70 else "尚可接受", delta_color="inverse")
        
        col1, col2 = st.columns(2)
        col1.info(f"**過去的承諾**：\n{cp['past_statement']}")
        col2.error(f"**今日的發言**：\n{cp['current_statement']}")
        st.markdown(f"> **龍雲無情點評**：{cp['judgment_summary']}")

    # 4. 預測未來 (拉普拉斯預言機)
    with tab4:
        st.header("🔮 來自未來的神諭")
        ld = matrix_data['laplace_demon']
        st.write(f"**預言機總結**：{ld['oracle_summary']}")
        
        st.progress(ld['probability_1'] / 100, text=f"機率 {ld['probability_1']}% - {ld['prediction_1']}")
        st.progress(ld['probability_2'] / 100, text=f"機率 {ld['probability_2']}% - {ld['prediction_2']}")
        st.progress(ld['probability_3'] / 100, text=f"機率 {ld['probability_3']}% - {ld['prediction_3']}")

    # 5. 創世解答 (跨維度創世引擎)
    with tab5:
        st.header("🧬 巔峰科技的狂妄融合")
        ge = matrix_data['genesis_engine']
        st.subheader(f"💡 顛覆性產品：{ge['new_product_name']}")
        st.metric("華爾街預估初始估值", ge['estimated_valuation'])
        
        col1, col2 = st.columns(2)
        col1.success(f"**融合技術 A**：{ge['fused_tech_a']}")
        col2.success(f"**融合技術 B**：{ge['fused_tech_b']}")
        st.info(f"**產品架構與商業模式**：\n{ge['architecture_description']}")

else:
    st.warning("⚠️ 矩陣尚未啟動，請手動執行 `python daily_cron.py` 讓大腦進行第一次全知運算！")
    if matrix_data and "error" in matrix_data:
        st.error(matrix_data["error"])