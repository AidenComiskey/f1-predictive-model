import pandas as pd

# load csv into dataframe
df = pd.read_csv("data/combined_data.csv")

# Analyse data to see what columns are in the dataset and how many null values there are and where about
print(df.head())
#print(df.info())
print(df.isnull().sum())


df = df.drop(columns=["DriverNumber_quali", "TeamName_quali", "Circuit_quali"])

print("before drop na", df.shape)
df = df.dropna()
print("after drop na", df.shape)

df.loc[df["GridPosition"] == 0, "GridPosition"] = 21
print(df["GridPosition"].value_counts().sort_index())

df.to_csv("data/basic_combined_data_clean.csv", index=False)
