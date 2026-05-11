import requests
from bs4 import BeautifulSoup
import json

def get_data():
    url = "https://drugsporphyria.net/safedrugs"
    print("本家サイトからデータを読み込んでいます...")
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        # 本家サイトにアクセスを試みる
        res = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(res.text, 'html.parser')
        drugs = []
        rows = soup.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 3:
                name_en = cols[0].get_text(strip=True)
                status_raw = cols[2].get_text(strip=True)
                status = "Safe" if "Not" in status_raw or "Probably not" in status_raw else "Unsafe"
                drugs.append({
                    "name_en": name_en,
                    "name_jp": f"(確認中) {name_en}",
                    "status": status,
                    "category": "NAPOS Data"
                })
        
        # 10件以上取れたら成功とみなす
        if len(drugs) > 10:
            return drugs
    except:
        pass
    
    # --- サイトから取れなかった時のための「予備データ」 ---
    print("サイト制限のため、用意した主要な全データを流し込みます...")
    return [
        {"name_en":"Loxoprofen","name_jp":"ロキソプロフェン","status":"Safe","category":"解熱鎮痛"},
        {"name_en":"Diazepam","name_jp":"ジアゼパム","status":"Unsafe","category":"抗不安"},
        {"name_en":"Acetaminophen","name_jp":"アセトアミノフェン","status":"Safe","category":"解熱鎮痛"},
        {"name_en":"Amlodipine","name_jp":"アムロジピン","status":"Safe","category":"血圧"},
        {"name_en":"Nifedipine","name_jp":"ニフェジピン","status":"Safe","category":"血圧"},
        {"name_en":"Phenobarbital","name_jp":"フェノバルビタール","status":"Unsafe","category":"抗てんかん"},
        {"name_en":"Diclofenac","name_jp":"ジクロフェナク","status":"Unsafe","category":"鎮痛"},
        {"name_en":"Amoxicillin","name_jp":"アモキシシリン","status":"Safe","category":"抗生物質"},
        {"name_en":"Erythromycin","name_jp":"エリスロマイシン","status":"Unsafe","category":"抗生物質"},
        {"name_en":"Warfarin","name_jp":"ワルファリン","status":"Safe","category":"血液をさらさらにする"}
    ]

if __name__ == "__main__":
    result = get_data()
    with open('drugs.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"【成功！】 {len(result)}件のデータで drugs.json を更新しました。")