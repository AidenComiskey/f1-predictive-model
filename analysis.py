import pandas as pd

# load csv into dataframe
df = pd.read_csv("enhanced_data/combined_data.csv")

# Analyse data to see what columns are in the dataset and how many null values there are and where about
print(df.head())
#print(df.info())
print(df.isnull().sum())

# make sure bestlap_sec is a number not a string and fill the missing values with the median
df['BestLap_Sec'] = pd.to_numeric(df['BestLap_Sec'], errors='coerce')
median_best_lap = df['BestLap_Sec'].median()
df['BestLap_Sec'] = df['BestLap_Sec'].fillna(median_best_lap)

# grid position 0.0 represents pit lane start in fastf1 api
# so changing it to 21 shows it is worse than starting last and makes it more accurate
df.loc[df["GridPosition"] == 0, "GridPosition"] = 21
print(df["GridPosition"].value_counts().sort_index())

# drop null values from the dataset
df = df.dropna(subset=["GridPosition", "Position_race", "Position_quali"])

# team names have changed through the years so need to be made the same throughout the dataset
team_mapping = {
    "Force India": "Aston Martin",
    "Racing Point": "Aston Martin",
    "Renault": "Alpine",
    "Toro Rosso": "Racing Bulls",
    "Red Bull Racing": "Red Bull Racing",
    "McLaren": "McLaren",
    "Ferrari": "Ferrari",
    "Mercedes": "Mercedes",
    "Williams": "Williams",
    "Sauber": "Kick Sauber",
    "Alfa Romeo": "Kick Sauber",
    "Aston Martin": "Aston Martin",
    "Alpine": "Alpine",
    "AlphaTauri": "Racing Bulls",
    "Haas F1 Team": "Haas F1 Team",
    "Kick Sauber": "Kick Sauber",
    "RB": "Racing Bulls",
    "Alfa Romeo Racing": "Kick Sauber"
}

# replace all team names with the ones from the dictionary so there are the 10 teams
df["TeamName_race"] = df["TeamName_race"].replace(team_mapping)

circuit_mapping = {
    "Monaco": "Monte Carlo",
    "Marina Bay": "Singapore",
    "Yas Island": "Yas Marina"
}

df["Circuit_race"] = df["Circuit_race"].replace(circuit_mapping)

#print(f"nulls after cleaning: {df.isnull().sum()}")

track_df = pd.read_csv("enhanced_data/track_info.csv")
df = df.merge(track_df, left_on='Circuit_race', right_on='Circuit', how='left')

df['PositionDelta'] = df['Position_race'] - df['GridPosition']

# sort so past races come before current ones
df = df.sort_values(['Abbreviation', 'Year', 'Round'])

# rolling mean of last 3 races for each driver
df['DriverForm'] = (
    df.groupby('Abbreviation')['Position_race']
      .transform(lambda x: x.shift().rolling(3, min_periods=1).mean())
)


df['DriverCircuitForm'] = (
    df.groupby(['Abbreviation', 'Circuit_race'])['Position_race']
      .transform(lambda x: x.shift().rolling(3, min_periods=1).mean())
)

# Team rolling form (last 3 races)
df['TeamForm'] = (
    df.groupby('TeamName_race')['Position_race']
      .transform(lambda x: x.shift().rolling(3, min_periods=1).mean())
)

# Rookie race flag (first race for each driver)
df['IsRookieRace'] = df.groupby('Abbreviation').cumcount() == 0
df['IsRookieRace'] = df['IsRookieRace'].astype(int)

# New circuit flag (first race for each driver at this circuit)
df['IsNewCircuit'] = (
    df.groupby(['Abbreviation', 'Circuit_race']).cumcount() == 0
)
df['IsNewCircuit'] = df['IsNewCircuit'].astype(int)

df = df.sort_values(['Year', 'Round', 'Position_race']).reset_index(drop=True)

# drop columns not needed
df = df.drop(columns=["DriverNumber_quali", "TeamName_quali", "Circuit_quali", 'Circuit_race', 'Country'])
print(df.isnull().sum())
df.to_csv("enhanced_data/combined_data_clean.csv", index=False)
