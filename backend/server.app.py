from flask import Flask, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

BASE_URL = "https://api.zeroc.green/v1/stations/"


@app.route("/api/stations/<station_id>")
def get_station_details(station_id):
    print(f" Richiesta ricevuta per ID: {station_id}")
    try:
        #  Richiesta API esterna
        resp = requests.get(f"{BASE_URL}{station_id}", timeout=10)
        resp.raise_for_status()
        data = resp.json()

        #  Cicla su ogni metrica e calcola media ponderata
        for metric in data.get("metrics", []):
            values = metric.get("data_points", [])

            #  Prendi solo gli ultimi 10 giorni (come da specifica)
            last_10_days = values[-10:]

            # Filtra solo i giorni validi con sample_size > 0
            valid_days = [v for v in last_10_days if v.get("sample_size", 0) > 0]

            #  Prendi gli ultimi 7 giorni disponibili
            last_7_days = valid_days[-7:]

            
            if last_7_days:
                total_weight = sum(v["sample_size"] for v in last_7_days)
                weighted_sum = sum(v["average"] * v["sample_size"] for v in last_7_days)
                weighted_avg = weighted_sum / total_weight if total_weight > 0 else None
            else:
                weighted_avg = None  

            
            metric["weighted_avg"] = weighted_avg

        return jsonify(data)

    except requests.RequestException as e:
        return jsonify({"error": f"Errore nel recupero stazione: {str(e)}"}), 500



@app.route("/api/stations")
def get_stations():
    
    try:
        
        resp = requests.get(f"{BASE_URL}", timeout=10)
        resp.raise_for_status()
        data = resp.json()

        
        stations = data.get("stations", data)
        return jsonify(stations)
    except requests.RequestException as e:
        return jsonify({"error": f"Errore nel recupero stazioni: {str(e)}"}), 500





if __name__ == "__main__":
    app.run(debug=True)
