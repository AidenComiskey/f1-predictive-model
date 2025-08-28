import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, classification_report

df = pd.read_csv("enhanced_data/combined_data_clean.csv")

le_driver = LabelEncoder()
le_team = LabelEncoder()
le_circuit = LabelEncoder()

df['Driver_to_num'] = le_driver.fit_transform(df['Abbreviation'])
df['Team_to_num'] = le_team.fit_transform(df['TeamName_race'])
df['Circuit_to_num'] = le_circuit.fit_transform(df["Circuit_race"])

df['Podium'] = df['Position_race'].apply(lambda x: 1 if x <= 3 else 0)

features = ['Position_quali', 'GridPosition', 'Driver_to_num', 
            'Team_to_num', 'Circuit_to_num', 'IsWetRace', 'IsWetQuali', 'BestLap_Sec']

X = df[features]
y = df['Podium']

X_test, X_train, y_test, y_train = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

model = XGBClassifier(
    n_estimators=300, 
    learning_rate=0.1, 
    max_depth=5, 
    random_state=42,
    use_label_encoder=False,
    eval_metric='logloss'
)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print(f"Podium classification accuracy: {accuracy:.3f}")
print(classification_report(y_test, y_pred))

