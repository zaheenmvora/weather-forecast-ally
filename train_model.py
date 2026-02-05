import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Load dataset
df = pd.read_csv('rain_india.csv')
print("Dataset loaded:", df.shape)

# Clean
df = df.dropna()
df['RainToday'] = df['RainToday'].map({'Yes': 1, 'No': 0})
df['RainTomorrow'] = df['RainTomorrow'].map({'Yes': 1, 'No': 0})
df = df.dropna()
print("After cleaning:", df.shape)

# Accuracy
X = df[['MinTemp', 'MaxTemp', 'Humidity9am', 'Humidity3pm',
        'WindSpeed9am', 'WindSpeed3pm', 'RainToday']]
y = df['RainTomorrow']

# STRATIFIED SPLIT 
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# RANDOM FOREST
model = RandomForestClassifier(
    n_estimators=300,
    max_depth=10,
    min_samples_split=4,
    min_samples_leaf=2,
    random_state=42
)

model.fit(X_train, y_train)

# Results
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"\nAccuracy: {accuracy:.2%}")
print("\n📊 CLASSIFICATION REPORT:")
print(classification_report(y_test, y_pred))

# Save
joblib.dump(model, 'weather_model.pkl')

