# -*- coding: utf-8 -*-
"""
Created on Sun May 17 18:03:55 2026

@author: ediso
"""

# 引入所需的開源套件
import requests
from bs4 import BeautifulSoup

def longyun_crawl(url):
    print(f"☁️ 龍雲正在伸出溯源觸角，掃描目標：{url} ...")
    try:
        # 模擬一般人類瀏覽器發送請求，避免被網站阻擋
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status() # 檢查連線是否成功

        # 使用 BeautifulSoup 啟動輕量過濾
        soup = BeautifulSoup(response.text, 'html.parser')

        # 抓取網頁標題
        title = soup.title.string if soup.title else "無標題"

        # 抓取網頁中所有的段落文字 (p 標籤)
        paragraphs = soup.find_all('p')
        
        # 將所有段落結合成純文字
        content = "\n".join([p.text.strip() for p in paragraphs if p.text.strip()])

        print("✨ 掃描完成！已成功剝離 HTML 骨架，提取純文字。")
        return {"title": title, "content": content}

    except Exception as e:
        print(f"⚠️ 觸角掃描失敗，遇到阻礙：{e}")
        return None

# --- 測試狩獵場 ---
# 這裡使用維基百科的「謠言」條目作為初始測試目標，你也可以換成任何你想測試的新聞或農場網址
target_url = "https://zh.wikipedia.org/wiki/%E8%AC%A0%E8%A8%80"
result = longyun_crawl(target_url)

if result:
    print("\n================ 龍雲抓取結果 ================")
    print(f"【標題】: {result['title']}")
    print(f"【內容片段】:\n{result['content'][:300]} ... (省略後續)")
    print("==============================================")