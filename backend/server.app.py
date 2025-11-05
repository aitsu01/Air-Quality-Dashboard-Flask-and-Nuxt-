from flask import Flask, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

BASE_URL = "https://api.zeroc.green/v1/stations/"


@app.route("/api/stations/<station_id>")
def get_station_details(station_id):
    try:
        resp = requests.get(f"https://api.zeroc.green/v1/stations/{station_id}", timeout=10)
        resp.raise_for_status()
        data = resp.json()

        # Calcolo media ponderata per ogni metrica (ultimi 7 giorni)
        for metric in data.get("metrics", []):
            values = metric.get("data_points", [])
            valid = [v for v in values[-7:] if v.get("sample_size", 0) > 0]
            if valid:
                total_weight = sum(v["sample_size"] for v in valid)
                weighted_avg = sum(v["average"] * v["sample_size"] for v in valid) / total_weight
            else:
                weighted_avg = None
            metric["weighted_avg"] = weighted_avg

        return jsonify(data)

    except requests.RequestException as e:
        return jsonify({"error": f"Errore nel recupero stazione: {str(e)}"}), 500


@app.route("/api/stations")
def get_stations():
    """Proxy per elenco stazioni"""
    try:
        # Chiamata diretta all'endpoint ufficiale
        resp = requests.get(f"{BASE_URL}", timeout=10)
        resp.raise_for_status()
        data = resp.json()

        # L'API restituisce {"stations": [...]} → estraiamo la lista
        stations = data.get("stations", data)
        return jsonify(stations)
    except requests.RequestException as e:
        return jsonify({"error": f"Errore nel recupero stazioni: {str(e)}"}), 500





if __name__ == "__main__":
    app.run(debug=True)

