import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, mean_absolute_error

df = pd.read_csv("enhanced_data/combined_data_clean.csv")

le_driver = LabelEncoder()
le_team = LabelEncoder()
le_circuit = LabelEncoder()

df['Driver_to_num'] = le_driver.fit_transform(df['Abbreviation'])
df['Team_to_num'] = le_team.fit_transform(df['TeamName_race'])
df['Circuit_to_num'] = le_circuit.fit_transform(df["Circuit_race"])

df_podium = df[df['Position_race'] <=3].copy()

features = ['Position_quali', 'GridPosition', 'Driver_to_num', 
            'Team_to_num', 'Circuit_to_num', 'IsWetRace', 'IsWetQuali', 'BestLap_Sec']

X = df_podium[features]
y = df_podium['Position_race'] 

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = XGBRegressor(
    n_estimators=300, 
    learning_rate=0.1, 
    max_depth=5, 
    random_state=42,
)

model.fit(X_train, y_train)

y_pred = np.rint(model.predict(X_test)).astype(int)

# Clip predictions to valid range (1,2,3)
y_pred = np.clip(y_pred, 1, 3)

# Evaluation
mae = mean_absolute_error(y_test, y_pred)

accuracy = accuracy_score(y_test, y_pred)
print(f"Mean absolute error: {mae:.3f}")
print(f"Exact Podium accuracy: {accuracy:.3f}")
print(classification_report(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))

