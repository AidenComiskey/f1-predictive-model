import pandas as pd

# load csv into dataframe
df = pd.read_csv("data/combined_data.csv")

# Analyse data to see what columns are in the dataset and how many null values there are and where about
print(df.head())
#print(df.info())
print(df.isnull().sum())

# drop duplicate columns, dont need team name etc twice
df = df.drop(columns=["DriverNumber_quali", "TeamName_quali", "Circuit_quali"])

# drop null values from the dataset
print("before drop na", df.shape)
df = df.dropna()
print("after drop na", df.shape)

# grid position 0.0 represents pit lane start in fastf1 api
# so changing it to 21 shows it is worse than starting last and makes it more accurate
df.loc[df["GridPosition"] == 0, "GridPosition"] = 21
print(df["GridPosition"].value_counts().sort_index())

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

print(df["TeamName_race"].unique())

df.to_csv("data/basic_combined_data_clean.csv", index=False)
