# Weather Forecast Ally 🌦

A Machine Learning-based weather prediction web application that forecasts the probability of rain using live weather data and a trained Random Forest model. This project integrates real-time API data with predictive modeling to provide weather insights and intelligent activity recommendations.

## Features

- Live weather data using OpenWeather API  
- Rain prediction for tomorrow using Random Forest (≈88% accuracy)  
- Probability confidence visualization  
- Intelligent weather-based recommendations  
- Interactive and responsive Streamlit interface  

## Technologies Used

- Python  
- Scikit-learn (Random Forest Classifier)  
- Pandas  
- Joblib  
- PyOWM (OpenWeather API wrapper)  
- Streamlit  

## Getting Started

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/weather-forecast-ally.git
   cd weather-forecast-ally
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Add OpenWeather API key:**

   Create a folder named `.streamlit` and inside it create a file called `secrets.toml`:

   ```
   OWM_API_KEY = "your_api_key_here"
   ```

4. **Run the application:**
   ```bash
   streamlit run app.py
   ```

5. **Access the app:**
   The application will automatically open in your browser.

## Model Details

- Model: Random Forest Classifier  
- Train-Test Split: Stratified (80-20)  
- Feature Engineering: Temperature, Humidity, Wind Speed, RainToday  
- Accuracy: ~88%  
- Evaluated using Classification Report  

## Contributing

Contributions are welcome. Feel free to open issues or submit pull requests for improvements.

## Disclaimer

Weather predictions are based on historical data and probabilistic modeling. Results may not exactly match official meteorological forecasts.

## License

[MIT License](LICENSE)
