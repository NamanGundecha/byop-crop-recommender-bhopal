from flask import Flask, render_template, request
import pandas as pd
import numpy as np

app = Flask(__name__)

# Real Bhopal mandi data (from your CSV)
crops = {
    'Soyabean': {'price': 5451, 'yield': 18, 'soil': 'Black Soil'},
    'Wheat': {'price': 2668, 'yield': 22, 'soil': 'Alluvial Soil'}, 
    'Gram': {'price': 5800, 'yield': 15, 'soil': 'Laterite Soil'},
    'Maize': {'price': 2100, 'yield': 20, 'soil': 'Red Soil'},
    'Rapeseed': {'price': 4800, 'yield': 16, 'soil': 'Black Soil'}
}

soils = {'Black Soil': 1.2, 'Red Soil': 1.0, 'Alluvial Soil': 1.1, 'Laterite Soil': 0.9}

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    if request.method == 'POST':
        temp = float(request.form['temp'])
        rain = float(request.form['rain'])
        hum = float(request.form['hum'])
        soil = request.form['soil']
        retention = soils[soil]
        
        # Smart scoring formula (no ML needed)
        for crop, data in crops.items():
            # Weather suitability
            temp_score = max(0, 1 - abs(temp - 28)/15)  # Optimal 28°C
            rain_score = min(1, rain/20) if 'Wheat' not in crop else max(0, 1-rain/10)
            soil_score = 1.2 if data['soil'] == soil else 0.8
            
            # Final profit score
            profit_score = (data['price'] * data['yield'] * temp_score * rain_score * soil_score * retention) / 10000 * 100
            results.append({'crop': crop, 'score': profit_score, 'price': data['price']})
        
        results = sorted(results, key=lambda x: x['score'], reverse=True)[:3]
    
    return render_template('index.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)