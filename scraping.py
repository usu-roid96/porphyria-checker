import requests
from bs4 import BeautifulSoup
import json

def get_data():
    url = "https://drugsporphyria.net/safedrugs"
    print("本家サイトから全データを取得しています...")
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        drugs = []
        rows = soup.select('table tr')
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 3:
                name_en = cols[0].get_text(strip=True)
                status_raw = cols[2].get_text(strip=True)
                status = "Safe" if "Not" in status_raw or "Probably not" in status_raw else "Unsafe"
                drugs.append({
                    "name_en": name_en,
                    "name_jp": f"（確認中）{name_en}",
                    "status": status,
                    "category": "NAPOS Data"
                })
        return drugs
    except Exception as e:
        print(f"エラー: {e}")
        return []

if __name__ == "__main__":
    result = get_data()
    if result:
        with open('drugs.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"【成功！】 {len(result)}件取得しました。")
        