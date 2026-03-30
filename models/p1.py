# Cell 1: Imports & Data Load
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

df_mandi = pd.read_csv('data/crops_mandi.csv')
df_weather = pd.read_csv('data/weather_bhopal.csv')
df_soil = pd.read_csv('data/soil_types_mp.csv')
print(df_mandi.head())

# Cell 2: Model Training (as executed above)
# ... (code from previous tool call)
# Outputs: Model saved with 1.00 train acc (overfits small data – real reflection point)
