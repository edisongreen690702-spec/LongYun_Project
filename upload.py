# -*- coding: utf-8 -*-
"""
Created on Sun May 17 21:26:54 2026

@author: ediso
"""

import os
import subprocess
import datetime

# ================= 龍雲的安全配置 =================
GITHUB_USERNAME = "edisongreen690702-spec"
GITHUB_REPO = "LongYun_Project"

# 🛡️ 龍雲防護：從 Windows 環境變數讀取金鑰，絕不留在程式碼中
GITHUB_TOKEN = os.getenv("LONGYUN_GITHUB_TOKEN")
# ====================================================

def run_git_command(command, check=True):
    """執行系統指令的輔助函式，並自帶密碼遮蔽防護"""
    try:
        # 為了避免指令字串中包含密碼被直接印出，我們使用 capture_output
        result = subprocess.run(command, shell=True, check=check, capture_output=True, text=True)
        return result
    except subprocess.CalledProcessError as e:
        error_msg = str(e.stderr) if e.stderr else str(e.stdout)
        # 貼心設計：如果發生錯誤，立刻把錯誤訊息裡的密碼打碼，保護你的安全
        if GITHUB_TOKEN:
            error_msg = error_msg.replace(GITHUB_TOKEN, "********")
        print(f"❌ 執行失敗: {command.replace(GITHUB_TOKEN, '********') if GITHUB_TOKEN else command}")
        print(f"⚠️ 錯誤訊息: {error_msg.strip()}")
        return None

def auto_upload():
    print("☁️ 龍雲正在啟動『神級零點擊·自動演化傳送門』...")
    
    if not GITHUB_TOKEN:
        print("\n❌ 傳送失敗：找不到系統環境變數 [LONGYUN_GITHUB_TOKEN]")
        print("💡 請先在 Windows 命令提示字元執行: set LONGYUN_GITHUB_TOKEN=你的金鑰")
        return

    # 1. 自動更新套件清單 (消化酶)
    #print("📋 正在更新套件清單 (requirements.txt)...")
    #run_git_command("pip freeze > requirements.txt")

    # 2. 結合創造者的神級 Git 版控邏輯
    print("🐙 正在結合神級 Git 版控邏輯...")
    repo_url = f"https://github.com/{GITHUB_USERNAME}/{GITHUB_REPO}.git"
    auth_repo_url = repo_url.replace("https://", f"https://{GITHUB_TOKEN}@")

    # 初始化或更新遠端網址
    if not os.path.exists(".git"):
        run_git_command("git init")
        run_git_command("git branch -M main")
        run_git_command(f"git remote add origin {auth_repo_url}")
    else:
        run_git_command(f"git remote set-url origin {auth_repo_url}")

    # 設置演化機器人的專屬身分
    run_git_command('git config user.email "longyun@evolution.bot"')
    run_git_command('git config user.name "LongYun Auto Deploy"')

    # 3. 打包與提交
    run_git_command("git add .")
    
    # 檢查是否有檔案變更
    status = run_git_command("git status --porcelain", check=False)
    if status and not status.stdout.strip():
        print("   ↳ 程式碼無變更，跳過 Commit。")
    else:
        commit_message = f"Evolution Auto-Sync: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        run_git_command(f'git commit -m "{commit_message}"')

    # 4. 核心魔法：動態金鑰注入與強制推送
    print("🚀 正在注入動態金鑰，光速推送至 GitHub (啟用強制覆寫模式)...")
    push_result = run_git_command("git push -f -u origin main")

    if push_result:
        print("\n✨ [數位飄移聲] 傳送完畢！大門已徹底擊碎，龍雲已成功抵達 GitHub！")

if __name__ == "__main__":
    auto_upload()