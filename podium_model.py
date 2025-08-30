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
le_type = LabelEncoder()
le_overtake = LabelEncoder()

df['Driver_to_num'] = le_driver.fit_transform(df['Abbreviation'])
df['Team_to_num'] = le_team.fit_transform(df['TeamName_race'])
df['Circuit_to_num'] = le_circuit.fit_transform(df["Circuit"])
df['Type_to_num'] = le_type.fit_transform(df["Type"])
df['OvertakingDifficulty_to_num'] = le_overtake.fit_transform(df['OvertakingDifficulty'])

df['RaceID'] = df['Year'].astype(str) + "_" + df['Round'].astype(str)

features = [
    'Position_quali', 'GridPosition', 'Driver_to_num', 'Team_to_num', 'Circuit_to_num',
    'IsWetRace', 'IsWetQuali', 'BestLap_Sec',
    'TrackLength_km', 'Corners', 'Type_to_num', 'OvertakingDifficulty_to_num',
    'DriverForm', 'DriverCircuitForm', 'TeamForm',
    'IsRookieRace', 'IsNewCircuit'
]

X = df[features]
y = df['Position_race'] 

#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

unique_races = df['RaceID'].unique()

train_races, test_races = train_test_split(unique_races, test_size=0.2, random_state=42)

train_df = df[df['RaceID'].isin(train_races)]
test_df = df[df['RaceID'].isin(test_races)]

X_train = train_df[features]
y_train = train_df['Position_race']

X_test = test_df[features]
y_test = test_df['Position_race']

model = XGBRegressor(
    n_estimators=300, 
    learning_rate=0.1, 
    max_depth=5, 
    random_state=42,
)

model.fit(X_train, y_train)

#y_pred = np.rint(model.predict(X_test)).astype(int)

# Clip predictions to valid range
#y_pred = np.clip(y_pred, 1, 20)
y_pred = model.predict(X_test)
# Evaluation
mae = mean_absolute_error(y_test, y_pred)

print(f"Mean absolute error: {mae:.3f}")
y_pred_train = model.predict(X_train)
mae_train = mean_absolute_error(y_train, y_pred_train)
print(f"Train MAE: {mae_train:.3f}")

podium_mask = y_test <= 3
y_test_podium = y_test[podium_mask]
y_pred_podium = y_pred[podium_mask]

# Mean Absolute Error for podium
mae_podium = mean_absolute_error(y_test_podium, y_pred_podium)
print(f"Podium MAE: {mae_podium:.3f}")

# For “exact podium prediction” accuracy
# Round predictions to nearest int and clip to 1-3
y_pred_podium_rounded = np.clip(np.rint(y_pred_podium), 1, 3).astype(int)
accuracy_podium = (y_pred_podium_rounded == y_test_podium).mean()
print(f"Exact podium accuracy: {accuracy_podium:.3f}")

podium_accuracy = 0
for race in test_races:
    race_mask = test_df['RaceID'] == race
    y_true_race = y_test[race_mask].values
    y_pred_race = np.rint(y_pred[race_mask]).astype(int)
    y_pred_race = np.clip(y_pred_race, 1, 3)
    
    # Only take podium (positions 1-3)
    y_true_podium = np.sort(y_true_race[y_true_race <= 3])
    y_pred_podium = np.sort(y_pred_race[y_true_race <= 3])
    
    if np.array_equal(y_true_podium, y_pred_podium):
        podium_accuracy += 1

exact_podium_acc = podium_accuracy / len(test_races)
print(f"Exact podium accuracy per race: {exact_podium_acc:.3f}")
