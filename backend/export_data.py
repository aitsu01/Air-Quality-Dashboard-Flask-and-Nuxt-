
import requests, json

station_id = "6059c8bc-69bf-4d9a-9c89-179f41e34972"
url = f"http://127.0.0.1:5000/api/stations/{station_id}"

print(f"📡 Recupero dati da: {url}")

resp = requests.get(url)
resp.raise_for_status()

data = resp.json()

with open("station_detail.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("✅ Dati completi salvati in station_detail.json")

