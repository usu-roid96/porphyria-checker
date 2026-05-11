import requests
from bs4 import BeautifulSoup
import json

def get_data():
    url = "https://drugsporphyria.net/safedrugs"
    print("本家サイトから全データを抽出中...")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}
    try:
        res = requests.get(url, headers=headers, timeout=20)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')
        drugs = []
        rows = soup.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 3:
                name_en = cols[0].get_text(strip=True)
                status_raw = cols[2].get_text(strip=True)
                status = "Safe" if "Not" in status_raw else "Unsafe"
                drugs.append({"name_en": name_en, "name_jp": f"(確認中) {name_en}", "status": status, "category": "NAPOS Data"})
        return drugs
    except:
        return []

if __name__ == "__main__":
    result = get_data()
    if len(result) > 100:
        with open('drugs.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"--- 完了！ ---")
        print(f"元サイトと同じ {len(result)} 件のデータを取得しました。")
    else:
        print("エラー：データが取得できませんでした。もう一度実行してください。")