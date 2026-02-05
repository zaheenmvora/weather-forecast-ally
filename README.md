Weather Forecast Ally 🌦

An AI-powered weather forecasting web application built using:

Streamlit

Random Forest (Scikit-Learn)

OpenWeather API

Python

🚀 Features

Live weather data using OpenWeather API

Rain prediction using ML model (88% accuracy)

Probability confidence bar

Intelligent activity recommendation system

Clean UI with responsive cards

🧠 Machine Learning

Random Forest Classifier

Stratified Train-Test Split

Feature Engineering

Accuracy: ~88%

📂 Project Structure
weather-predictor/
│
├── app.py
├── train_model.py
├── rain_india.csv
├── requirements.txt
└── README.md

⚙ Installation
git clone https://github.com/yourusername/weather-predictor.git
cd weather-predictor
pip install -r requirements.txt
streamlit run app.py

🔑 API Setup

Create a .streamlit/secrets.toml file:

OWM_API_KEY = "your_api_key_here"


Get API key from:
https://openweathermap.org/api

👨‍💻 Author

Zaheen M Vora
Aspiring Data Scientist & ML Engineer