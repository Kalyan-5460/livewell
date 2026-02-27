# 🌍 LivWell – Smart Livability Index

LivWell is an AI-powered web application that predicts whether a location is suitable for living using environmental data, nearby facilities, and machine learning.

---

## 🚀 Features
- 📍 Interactive Google Maps Integration
- 🌫️ Real-time Air Quality Index (OpenWeather API)
- 🏥 Nearby Facilities (Google Places API)
- 🤖 Machine Learning-based Livability Prediction
- 📊 City-level Environmental & Infrastructure Analysis
- 🖥️ Clean and Modern User Interface

---

## 🧠 Technologies Used

- Python (Flask)
- Scikit-learn (Random Forest Classifier)
- Pandas & NumPy
- Google Maps API
- OpenWeather API
- HTML, CSS, JavaScript, Bootstrap

---

## 📂 Project Structure

```
livewell/
│
├── app.py
├── model.pkl
├── final_dataset.csv
├── requirements.txt
├── templates/
│   └── index.html
├── static/
│   ├── css/
│   ├── js/
│   └── assets/
```

---

# 🛠️ How to Run the Project in VS Code

Follow these steps carefully:

---

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/livewell.git
cd livewell
```

---

## 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

This will create a folder called `venv`.

---

## 3️⃣ Activate Virtual Environment

### 🪟 Windows:
```bash
venv\Scripts\activate
```

### 🍎 Mac/Linux:
```bash
source venv/bin/activate
```

After activation, you should see:

```
(venv)
```

in your terminal.

---

## 4️⃣ Install Required Libraries

```bash
pip install -r requirements.txt
```

This installs all necessary dependencies.

---

## 5️⃣ Add API Keys

Open `app.py` and replace:

```python
app.config['GOOGLE_MAPS_API_KEY'] = "YOUR_GOOGLE_MAPS_API_KEY"
app.config['OPENWEATHER_API_KEY'] = "YOUR_OPENWEATHER_API_KEY"
```

With your actual API keys.

---

## 6️⃣ Run the Application

```bash
python app.py
```

You should see:

```
Running on http://127.0.0.1:5000
```

---

## 7️⃣ Open in Browser

Open:

```
http://127.0.0.1:5000
```

Your application will be running successfully 🎉

---

## ⚠️ Important Notes

- Make sure `model.pkl` is present in the root directory.
- Do NOT upload the `venv/` folder to GitHub.
- API keys should ideally be stored as environment variables for production deployment.

---

## 👨‍💻 Developed By

**Team Viveka**  
G.Ritvik
M.sarvagna
K.laxmi lavanya
M.K.V.Vinay

National Level Hackathon Project