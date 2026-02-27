from flask import Flask, render_template, request, jsonify
import requests
import pandas as pd
import joblib
import difflib

app = Flask(__name__)

# ---------------- CONFIG ----------------
app.config['GOOGLE_MAPS_API_KEY'] = "AIzaSyBEDZYrAqbXLIMh4z-HsyI9YyRI0QRAj3Q"
app.config['OPENWEATHER_API_KEY'] = "cfe48a7245126131a4ac309b754d03fa"

# ---------------- ML LOAD (ON STARTUP) ----------------
# Make sure these files are in the SAME folder as app.py:
# - final_dataset.csv
# - model.pkl
original_df = pd.read_csv("final_dataset.csv")
model, label_encoders, categorical_cols = joblib.load("model.pkl")


# ---------------- UTILITIES ----------------
def get_nearby_places(lat, lng, place_type, radius=1000):
    api_key = app.config['GOOGLE_MAPS_API_KEY']
    url = (
        "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        f"?location={lat},{lng}"
        f"&radius={radius}"
        f"&type={place_type}"
        f"&key={api_key}"
    )
    response = requests.get(url, timeout=15)
    results = response.json().get("results", [])

    places = []
    for place in results[:5]:  # Top 5
        places.append({
            "name": place.get("name"),
            "type": place_type,
            "vicinity": place.get("vicinity"),
            "distance_m": 500  # placeholder
        })
    return places


def get_real_aqi(lat, lon):
    api_key = app.config['OPENWEATHER_API_KEY']
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"

    response = requests.get(url, timeout=15)
    if response.status_code != 200:
        return {"aqi": "N/A", "pm25": "N/A", "last_updated": "N/A"}

    data = response.json()
    aqi_index = data["list"][0]["main"]["aqi"]  # 1–5 scale
    aqi_scaled = aqi_index * 20                # convert to 20–100 (your requirement)

    components = data["list"][0]["components"]
    pm25 = components.get("pm2_5", "N/A")

    return {
        "aqi": aqi_scaled,
        "pm25": pm25,
        "last_updated": "Real-Time"
    }


# ---------------- ROUTES ----------------
@app.route("/")
def index():
    return render_template("index.html", google_maps_api_key=app.config["GOOGLE_MAPS_API_KEY"])


@app.route("/api/livability")
def get_livability():
    lat = request.args.get("lat")
    lng = request.args.get("lng")

    if not lat or not lng:
        return jsonify({"error": "Missing coordinates"}), 400

    # AQI realtime
    aqi_data = get_real_aqi(lat, lng)

    components = {
        "aqi": aqi_data,
        "wqi": {"wqi": 85}  # dummy WQI for now
    }

    # Nearby places realtime (Google Places)
    facilities = []
    for place_type in ["hospital", "school", "grocery_or_supermarket"]:
        facilities.extend(get_nearby_places(lat, lng, place_type))

    result = {
        "score": 82,  # still dummy score (map summary)
        "category": "Good for Living",
        "components": {
            "aqi": components["aqi"],
            "wqi": components["wqi"],
            "facilities": facilities
        }
    }

    return jsonify(result)


# ---------------- ML PREDICTION ENDPOINT ----------------
@app.route("/api/predict")
def predict():
    city_name = request.args.get("city")

    if not city_name:
        return jsonify({"error": "City parameter is required"}), 400

    matches = original_df[original_df["City"].astype(str).str.lower() == city_name.lower()]

    if matches.empty:
        possible_cities = original_df["City"].astype(str).unique()
        close_matches = difflib.get_close_matches(city_name, possible_cities, n=3, cutoff=0.6)
        return jsonify({
            "error": f"City '{city_name}' not found",
            "suggestions": [str(c) for c in close_matches]
        }), 404

    city_original = matches.iloc[0]

    # Encode row for prediction
    encoded_row = city_original.copy()
    for col in categorical_cols:
        encoded_row[col] = label_encoders[col].transform([str(city_original[col])])[0]

    features = encoded_row.drop(["Livability Label", "Area ID"])

    prediction = model.predict([features])[0]
    livability = label_encoders["Livability Label"].inverse_transform([prediction])[0]

    # Return JSON with python native types
    result = {
        "city": str(city_original["City"]),
        "state": str(city_original["State"]),
        "aqi": float(city_original["AQI (%)"]),
        "wqi": float(city_original["WQI (%)"]),
        "water_quantity": float(city_original["Water Quantity (%)"]),
        "population_density": float(city_original["Population Density (%)"]),
        "industry_distance": float(city_original["Industry Distance (km)"]),
        "pollution": float(city_original["Pollution (%)"]),
        "cost_of_living": int(city_original["Cost of Living"]),
        "hospitals": int(city_original["Hospitals Nearby"]),
        "schools": int(city_original["Schools Nearby"]),
        "stores": int(city_original["Stores Nearby"]),
        "soil_type": str(city_original["Soil Type"]),
        "prediction": str(livability)
    }

    return jsonify(result)


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True, port=5000)