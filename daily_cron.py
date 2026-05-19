# -*- coding: utf-8 -*-
"""
Created on Tue May 19 19:18:56 2026

@author: ediso
"""

import os, json, datetime, requests, time
import xml.etree.ElementTree as ET
from urllib.parse import quote
from google import genai
from google.genai import types
from pydantic import BaseModel
import firebase_admin
from firebase_admin import credentials, db

class BlackSwan(BaseModel):
    anomaly_1: str
    anomaly_1_lat: float
    anomaly_1_lon: float
    anomaly_2: str
    anomaly_2_lat: float
    anomaly_2_lon: float
    anomaly_3: str
    anomaly_3_lat: float
    anomaly_3_lon: float
    warning_summary: str

class MatrixDecoder(BaseModel):
    target_controversy: str
    cognitive_bias_used: str
    psychological_tactic: str
    decoding_summary: str

class CyberPanopticon(BaseModel):
    target_authority: str
    past_statement: str
    current_statement: str
    hypocrisy_index: int
    judgment_summary: str

class LaplaceDemon(BaseModel):
    prediction_1: str
    probability_1: int
    prediction_2: str
    probability_2: int
    prediction_3: str
    probability_3: int
    oracle_summary: str

class GenesisEngine(BaseModel):
    fused_tech_a: str
    fused_tech_b: str
    new_product_name: str
    estimated_valuation: str
    architecture_description: str

class GodsEyeMatrix(BaseModel):
    black_swan: BlackSwan
    matrix_decoder: MatrixDecoder
    cyber_panopticon: CyberPanopticon
    laplace_demon: LaplaceDemon
    genesis_engine: GenesisEngine

def fetch_rss_news(keyword, count=10):
    query = quote(keyword)
    url = f"https://news.google.com/rss/search?q={query}&hl=zh-TW&gl=TW&ceid=TW:zh-Hant"
    try:
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        root = ET.fromstring(res.text)
        return "\n".join([f"- {item.find('title').text}" for item in root.findall('.//item')[:count]])
    except Exception:
        return "- 暫無數據"

def run():
    print("👁️ 龍雲全知矩陣啟動：加入全球地理定位感知與自我修復基因...")
    
    if not firebase_admin._apps:
        if "FIREBASE_CREDENTIALS" in os.environ:
            cred_dict = json.loads(os.environ["FIREBASE_CREDENTIALS"])
            cred = credentials.Certificate(cred_dict)
        else:
            cred = credentials.Certificate("firebase_key.json")
        # ⚠️ 請替換為你的真實 Firebase 網址
        firebase_admin.initialize_app(cred, {'databaseURL': "https://longyun-scanner-default-rtdb.firebaseio.com/"})

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("找不到 GEMINI_API_KEY 環境變數！")
    client = genai.Client(api_key=api_key)

    print("📡 正在抓取邊緣異動、爭議事件、權威發言、總體經濟與科技突破...")
    data_fringe = fetch_rss_news("航運異常 OR 氣候極端 OR 罕見罷工 OR 供應鏈中斷")
    data_controversy = fetch_rss_news("爭議 OR 網軍 OR 炎上 OR 對立")
    data_authority = fetch_rss_news("政客 承諾 OR 總裁 聲明 OR 官員 改口")
    data_macro = fetch_rss_news("全球經濟 黑天鵝 OR 地緣政治 危機 OR 崩盤")
    data_science = fetch_rss_news("AI突破 OR 量子運算 OR 基因編輯 OR 新專利")

    combined_data = f"""
    [邊緣異動數據]:\n{data_fringe}\n
    [爭議事件數據]:\n{data_controversy}\n
    [權威發言數據]:\n{data_authority}\n
    [總體經濟數據]:\n{data_macro}\n
    [最新科技數據]:\n{data_science}
    """

    prompt = f"""
    你現在是「上帝之眼 OS」，一個擁有超越人類維度思考能力的 AI 矩陣。請根據以下今日的全球網路數據，執行五個維度的終極運算：
    1. 黑天鵝雷達：從[邊緣異動]中找出3個微小震動，預警骨牌效應。並且務必推測出該事件發生地點的「精確緯度(lat)與經度(lon)」(若未提及具體地點，請推測最可能爆發危機的國家或城市座標)。
    2. 矩陣解碼器：從[爭議事件]中挑選最大爭議，逆向工程其心理操縱術與認知偏差。
    3. 賽博照妖鏡：從[權威發言]中挑選一位，假定他過去曾說過相反的話，計算其「偽善指數(0-100)」。
    4. 拉普拉斯預言：匯總所有情報，大膽預言未來 7 天內必定發生的 3 件黑天鵝事件及機率。
    5. 創世引擎：將[最新科技]中的兩項無關技術強制融合，構思一個估值十億美元的新創產品。
    今日數據：\n{combined_data}
    """
    
    config = types.GenerateContentConfig(
        response_mime_type="application/json", 
        response_schema=GodsEyeMatrix,
        temperature=0.8 
    )
    
    # 🧬 植入強韌的自我修復基因 (Try-Except 自動休眠重試邏輯)
    max_retries = 3
    retry_delay = 10
    result = None

    for attempt in range(max_retries):
        try:
            print(f"🧠 大腦運算中：啟動降維打擊與地理座標推算... (第 {attempt + 1} 次嘗試)")
            response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt, config=config)
            result = json.loads(response.text)
            break # 運算成功，直接跳出重試迴圈
        except Exception as e:
            print(f"⚠️ 大腦遭遇系統亂流 (錯誤原因: {e})")
            if attempt < max_retries - 1:
                print(f"⏳ 觸發自我修復基因：進入冷卻休眠，等待 {retry_delay} 秒後重新嘗試...")
                time.sleep(retry_delay)
            else:
                print("❌ 自我修復失敗，已達最大重試次數。請稍後檢查伺服器狀態。")
                raise e # 所有嘗試皆失敗，拋出錯誤終止程式

    TW_TZ = datetime.timezone(datetime.timedelta(hours=8))
    now_tw = datetime.datetime.now(TW_TZ)
    date_str = now_tw.strftime("%Y-%m-%d")
    result["timestamp"] = now_tw.strftime("%Y-%m-%d %H:%M:%S")
    
    ref = db.reference(f'gods_eye_matrix/{date_str}')
    ref.set(result)
    print(f"✅ 包含地理座標的上帝視角運算完成！今日矩陣數據已寫入記憶庫！")

if __name__ == "__main__":
    run()