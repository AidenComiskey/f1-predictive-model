import pandas as pd

# load csv into dataframe
df = pd.read_csv("data/combined_data.csv")

# Analyse data to see what columns are in the dataset and how many null values there are and where about
print(df.head())
#print(df.info())
print(df.isnull().sum())


df = df.drop(columns=["DriverNumber_quali", "TeamName_quali", "Circuit_quali"])
print(df.info())