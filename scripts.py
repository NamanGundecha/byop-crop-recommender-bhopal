import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import numpy as np
import io

# Load data
df_mandi = pd.read_csv('output/crops_mandi.csv')
df_weather = pd.read_csv('output/weather_bhopal.csv')
df_soil = pd.read_csv('output/soil_types_mp.csv')

# Simulate features for model: temp, rain, humidity, price, retention
np.random.seed(42)
crops = ['Soyabean', 'Wheat', 'Gram', 'Maize', 'Rapeseed']
data = []
for _ in range(100):
    crop = np.random.choice(crops)
    temp = np.random.uniform(15, 40)
    rain = np.random.uniform(0, 50)
    hum = np.random.uniform(50, 90)
    price = df_mandi[df_mandi['crop']==crop]['price_per_quintal'].iloc[0] if not df_mandi[df_mandi['crop']==crop].empty else 3000
    retention = np.random.choice([0.9,1.0,1.1,1.2])
    profit_score = (price * retention * (1 - abs(25-temp)/25) * (rain/20 if rain<20 else 0.8))  # Dummy formula
    data.append([temp, rain, hum, price, retention, profit_score > np.mean([d[5] for d in data]) if data else True])

df_train = pd.DataFrame(data, columns=['temp', 'rain', 'hum', 'price', 'retention', 'high_profit'])
X = df_train.drop('high_profit', axis=1)
y = df_train['high_profit']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model = RandomForestClassifier(n_estimators=50)
model.fit(X_train, y_train)

joblib.dump(model, 'output/crop_recommender.pkl')
print(f"Model saved. Train acc: {model.score(X_train, y_train):.2f}, Test acc: {model.score(X_test, y_test):.2f}")
print("Sample input prediction:")
sample = np.array([[32, 5, 65, 5451, 1.2]])
pred = model.predict(sample)
print(f"High profit prediction: {pred[0]}")
