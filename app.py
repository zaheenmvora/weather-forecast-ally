import streamlit as st
from pyowm import OWM
from datetime import datetime, date
import joblib
import pandas as pd
import random

def info_box(title, value, unit="", emoji=""):
    st.markdown(
        f"""
        <div style="
            border:1px solid #ddd;
            border-radius:12px;
            padding:18px;
            text-align:center;
            box-shadow:2px 2px 10px rgba(0,0,0,0.1);
            background-color:#ffffff;
            color:#000000;
        ">
            <div style="font-size:18px; font-weight:600;">
                {emoji} {title}
            </div>
            <div style="font-size:28px; margin-top:8px; font-weight:700;">
                {value} {unit}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Manual AI Recommendation
def generate_ai_recommendation(temp, rain_prob, humidity, wind, city):
    hour = datetime.now().hour
    is_night = hour >= 19 or hour <= 6
    is_morning = 6 < hour <= 11
    is_afternoon = 11 < hour <= 17
    is_evening = 17 < hour < 19

    recommendations = []

    # Rain logic
    if rain_prob > 80:
        recommendations.extend([
            "Heavy rain expected — a perfect day to stay indoors, enjoy movies, and sip on hot chai ☕.",
            "Rainy weather ahead — ideal for reading, cooking comfort food, or relaxing at home.",
            "With strong chances of rain, outdoor plans are best postponed today."
        ])
    elif 40 < rain_prob <= 80:
        recommendations.extend([
            "Light rain possible — carry an umbrella and enjoy calm indoor or café activities.",
            "Mild showers may occur — suitable for short walks and cozy indoor moments.",
            "Unpredictable rain today — flexible plans are recommended."
        ])
    else:
        recommendations.extend([
            "Clear skies expected — great conditions for outdoor activities.",
            "Low rain probability — a good day to plan travel or outdoor work.",
            "Dry weather ahead — ideal for daily routines and commuting."
        ])

    # Temperature logic
    if temp >= 38:
        recommendations.extend([
            "Extreme heat detected — stay hydrated and avoid stepping out during midday.",
            "Hot weather conditions — best to remain indoors and limit physical activity.",
            "High temperatures today — cooling drinks and shaded areas are recommended."
        ])
    elif 30 <= temp < 38:
        recommendations.extend([
            "Warm weather — suitable for light outdoor activities and office work.",
            "Moderately hot day — plan outdoor tasks during early morning or evening.",
            "Warm conditions — dress light and stay hydrated."
        ])
    elif 20 <= temp < 30:
        recommendations.extend([
            "Pleasant temperature — perfect for picnics, walks, or outdoor sports 🌳.",
            "Comfortable weather — an ideal day to socialize or explore the city.",
            "Balanced climate — suitable for both work and leisure activities."
        ])
    else:
        recommendations.extend([
            "Cool weather — a great excuse for warm beverages and cozy clothing.",
            "Lower temperatures — ideal for relaxed walks and indoor activities.",
            "Chilly conditions — enjoy hot food and minimal outdoor exposure."
        ])

    # Wind logic
    if wind > 7:
        recommendations.extend([
            "Windy conditions — avoid open areas and secure loose belongings.",
            "Strong winds today — outdoor activities may feel uncomfortable.",
            "High wind speed detected — drive carefully and stay alert."
        ])
    else:
        recommendations.extend([
            "Mild wind conditions — comfortable for outdoor movement.",
            "Light breeze — pleasant for walking and commuting."
        ])

    # Time logic
    if is_morning:
        recommendations.extend([
            "Fresh morning hours — perfect for exercise, walking, or planning the day.",
            "Morning weather feels refreshing — ideal for productivity and focus."
        ])
    elif is_afternoon:
        recommendations.extend([
            "Afternoon conditions suggest staying hydrated and avoiding direct sunlight.",
            "Midday weather — a good time for indoor work and breaks."
        ])
    elif is_evening:
        recommendations.extend([
            "Pleasant evening atmosphere — great for outings or spending time with friends.",
            "Evening hours feel calm — suitable for walks or light activities."
        ])
    elif is_night:
        recommendations.extend([
            "Peaceful night weather — unwind with music, movies, or relaxation 🌙.",
            "Late hours — best for rest and light indoor activities."
        ])

    # Localized wrap-up
    recommendations.extend([
        f"Overall, today’s weather in {city} supports a comfortable and balanced day.",
        f"Considering current conditions in {city}, plan your activities mindfully.",
        f"The atmosphere in {city} feels suitable for regular daily routines."
    ])

    return random.choice(recommendations)

API_KEY = st.secrets["OWM_API_KEY"]
owm = OWM(API_KEY)
model = joblib.load("weather_model.pkl")

st.title("Forecast Ally")
city_name = st.text_input("City:", )

if not city_name or city_name.lower() in [' ', '', 'none', 'null']:
        st.warning(" Please enter a valid city name .")
        st.stop() 

try:
    # Weather
    mgr = owm.weather_manager()
    observation = mgr.weather_at_place(city_name)
    forecast = mgr.forecast_at_place(city_name, '3h')
    forecast_weathers = forecast.forecast.weathers
    we = observation.weather

    current_temp = we.temperature("celsius")["temp"]
    humidity = we.humidity
    wind = we.wind()["speed"]

    today = date.today()

    today_temps = [current_temp]

    today_temps.extend([
        w.temperature('celsius')['temp']
        for w in forecast_weathers
        if w.reference_time('date').date() == today
    ])

    if today_temps:
        min_temp = round(min(today_temps), 1)
        max_temp = round(max(today_temps), 1)
    else:
        min_temp = round(current_temp, 1)
        max_temp = round(current_temp, 1)

    # ML Prediction
    features = pd.DataFrame({
        "MinTemp": [current_temp - 10],
        "MaxTemp": [current_temp + 12],
        "Humidity9am": [humidity],
        "Humidity3pm": [humidity + 5],
        "WindSpeed9am": [wind],
        "WindSpeed3pm": [wind + 2],
        "RainToday": [0]
    })

    rain_prob = model.predict_proba(features)[0][1] * 100
    st.markdown("### Rain Prediction ")

    if rain_prob >= 50:
        st.error(f"☔ **RAIN EXPECTED TOMORROW** ")
    else:
        st.success(f"☀️ **NO RAIN EXPECTED TOMORROW** ")
    
    bar_color = "#ff4b4b" if rain_prob >= 50 else "#2ecc71"
    st.markdown(
            f"""
            <div style="margin-top:10px;">
                <div style="
                    background-color:#e0e0e0;
                    border-radius:10px;
                    height:12px;
                    overflow:hidden;
                ">
                    <div style="
                        height:100%;
                        width:{rain_prob:.0f}%;
                        background-color:{bar_color};
                        border-radius:10px;
                        transition:width 1.5s ease-in-out;
                    ">
                    </div>
                </div>
                <div style="
                    text-align:center;
                    font-size:12px;
                    margin-top:4px;
                    font-weight:600;
                ">
                    Confidence: {rain_prob:.0f}%
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("### Current Weather Overview")

    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        info_box("Current Temp", f"{current_temp:.1f}", "°C", "🌡")

    with col2:
        info_box("Min Temp", f"{min_temp:.1f}", "°C", "⬇")

    with col3:
        info_box("Max Temp", f"{max_temp:.1f}", "°C", "⬆")

    with col4:
        info_box("Humid", humidity, "%", "💧")

    with col5:
        info_box("Wind Speed", f"{wind:.1f}", "m/s", "🌬")

    with col6:
        info_box("Rain Chance", f"{rain_prob:.0f}", "%", "🌧")

        
    st.markdown("### Intelligent Weather Recommendation")

    ai_recommendation = generate_ai_recommendation(
        current_temp,
        rain_prob,
        humidity,
        wind,
        city_name
    )

    st.success(ai_recommendation)

except Exception as e:
    st.error(f"Error: {str(e)}")

st.markdown("*By Zaheen M Vora*")

st.markdown(
    """
    <div style="
        text-align:center;
        font-size:12px;
        color:#777;
        margin-top:20px;
    ">
        ℹ Min & Max temperatures are based on forecast data from OpenWeather 
        and may slightly differ from official website values.
    </div>
    """,
    unsafe_allow_html=True
)

