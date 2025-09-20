import pandas as pd
import numpy as np
import joblib
from main import get_quali_results, get_race_results

# Load trained model and encoders
model = joblib.load("f1_position_model.pkl")
le_driver = joblib.load("encoders/le_driver.pkl")
le_team = joblib.load("encoders/le_team.pkl")
le_circuit = joblib.load("encoders/le_circuit.pkl")
le_type = joblib.load("encoders/le_type.pkl")
le_overtake = joblib.load("encoders/le_overtake.pkl")

# Load track info
track_df = pd.read_csv("enhanced_data/track_info.csv")

def update_dataset(year, round_number):
    """Fetch the last race results and append to dataset."""
    df_clean = pd.read_csv("enhanced_data/combined_data_clean.csv")
    
    # Avoid duplicate appends
    if not ((df_clean["Year"] == year) & (df_clean["Round"] == round_number)).any():
        print(f"Adding results for {year} Round {round_number}")
        new_race = get_race_results(year, round_number)  # you'll need this function
        df_clean = pd.concat([df_clean, new_race], ignore_index=True)
        df_clean.to_csv("enhanced_data/combined_data_clean.csv", index=False)
    else:
        print(f"Results for {year} Round {round_number} already in dataset.")

def predict_race_podium(year, round_number, circuit_name):
    # Get qualifying results

    if round_number > 1:
        update_dataset(year, round_number - 1)
    
    # (re)load dataset with latest results
    df_clean = pd.read_csv("enhanced_data/combined_data_clean.csv")

    qualiresult = get_quali_results(year, round_number)
    
    # Grid position is usually same as quali position
    qualiresult['GridPosition'] = qualiresult['Position']
    
    # Add track info
    track = track_df[track_df['Circuit'] == circuit_name].iloc[0]
    qualiresult['TrackLength_km'] = track['TrackLength_km']
    qualiresult['Corners'] = track['Corners']
    qualiresult['Type'] = track['Type']
    qualiresult['OvertakingDifficulty'] = track['OvertakingDifficulty']
    
    # Race conditions
    qualiresult['IsWetRace'] = 0
    qualiresult['IsWetQuali'] = 0
    
    # Calculate driver form (rolling avg last 3 races)
    driver_forms = []
    driver_circuit_forms = []
    team_forms = []
    for idx, row in qualiresult.iterrows():
        driver = row['Abbreviation']
        team = row['TeamName']
        
        # Driver form
        past_races = df_clean[df_clean['Abbreviation'] == driver]
        driver_form = past_races['Position_race'].tail(3).mean() if not past_races.empty else df_clean['Position_race'].mean()
        driver_forms.append(driver_form)
        
        # Driver circuit form
        past_circuit = past_races[past_races['Circuit'] == circuit_name]
        driver_circuit_form = past_circuit['Position_race'].tail(3).mean() if not past_circuit.empty else driver_form
        driver_circuit_forms.append(driver_circuit_form)
        
        # Team form
        past_team = df_clean[df_clean['TeamName_race'] == team]
        team_form = past_team['Position_race'].tail(3).mean() if not past_team.empty else df_clean['Position_race'].mean()
        team_forms.append(team_form)
    
    qualiresult['DriverForm'] = driver_forms
    qualiresult['DriverCircuitForm'] = driver_circuit_forms
    qualiresult['TeamForm'] = team_forms
    
    # Flags
    qualiresult['IsRookieRace'] = qualiresult['Abbreviation'].apply(lambda x: 1 if x not in df_clean['Abbreviation'].unique() else 0)
    qualiresult['IsNewCircuit'] = qualiresult['Abbreviation'].apply(lambda x: 1 if circuit_name not in df_clean[df_clean['Abbreviation']==x]['Circuit'].values else 0)
    
    # Encode categorical features using the saved encoders
    qualiresult['Driver_to_num'] = le_driver.transform(qualiresult['Abbreviation'])
    qualiresult['Team_to_num'] = le_team.transform(qualiresult['TeamName'])
    qualiresult['Circuit_to_num'] = le_circuit.transform([circuit_name]*len(qualiresult))
    qualiresult['Type_to_num'] = le_type.transform(qualiresult['Type'])
    qualiresult['OvertakingDifficulty_to_num'] = le_overtake.transform(qualiresult['OvertakingDifficulty'])

    qualiresult.rename(columns={'Position': 'Position_quali'}, inplace=True)

    
    # Feature list
    features = [
        'Position_quali', 'GridPosition', 'Driver_to_num', 'Team_to_num', 'Circuit_to_num',
        'IsWetRace', 'IsWetQuali', 'BestLap_Sec',
        'TrackLength_km', 'Corners', 'Type_to_num', 'OvertakingDifficulty_to_num',
        'DriverForm', 'DriverCircuitForm', 'TeamForm',
        'IsRookieRace', 'IsNewCircuit'
    ]
    
    X_new = qualiresult[features]
    y_pred = model.predict(X_new)
    qualiresult['PredictedPosition'] = np.clip(np.rint(y_pred), 1, 20).astype(int)
    
    # Sort to get predicted podium
    podium = qualiresult.sort_values('PredictedPosition').head(3)
    print("Predicted Podium:")
    for i, row in enumerate(podium.itertuples(), 1):
        print(f"{i}: {row.Abbreviation}")
    
    return podium

# Example usage
predicted_podium = predict_race_podium(2025, 17, "Baku")
