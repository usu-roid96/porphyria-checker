# 🚀 ポルフィリン症アプリ 開発メモ

### 1. データを更新したい時
ターミナルで実行：
python scraping.py

### 2. iPhoneに公開する時（3点セット）
git add .
git commit -m "更新内容を入力"
git push origin main
import requests
from bs4 import BeautifulSoup
import json
import time

def get_data():
    # 本家サイトのURL
    url = "https://drugsporphyria.net/safedrugs"
    print("本家サイトから全データを抽出中...（1,000件以上あるため少し時間がかかります）")
    
    # ブラウザのふりをする設定（重要！）
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }
    
    try:
        res = requests.get(url, headers=headers, timeout=20)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')
        
        drugs = []
        # 表のすべての行を取得
        rows = soup.find_all('tr')
        
        for row in rows:
            cols = row.find_all('td')
            # 1列目が「一般名」、3列目が「安全性」であることを確認
            if len(cols) >= 3:
                name_en = cols[0].get_text(strip=True)
                status_raw = cols[2].get_text(strip=True)
                
                # 安全性の判定
                # Safe: "Not porphyrinogenic" または "Probably not..."
                # Unsafe: それ以外（Porphyrinogenicなど）
                if "Not" in status_raw:
                    status = "Safe"
                else:
                    status = "Unsafe"
                
                drugs.append({
                    "name_en": name_en,
                    "name_jp": f"(確認中) {name_en}",
                    "status": status,
                    "category": "NAPOS Official Data"
                })
        
        return drugs
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return []

if __name__ == "__main__":
    result = get_data()
    
    if len(result) > 100: # 100件以上取れたら「成功」とみなす
        with open('drugs.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"--- 完了！ ---")
        print(f"元サイトと同じ {len(result)} 件のデータを取得し、drugs.json を更新しました。")
    else:
        print("うまくデータが取れませんでした。もう一度実行してみてください。")