import pandas as pd
import glob

#combine all years into two dataframes for all race results and all quali results

race_df = pd.concat([pd.read_csv(f) for f in glob.glob("data/race_results_*.csv")], ignore_index=True)
quali_df = pd.concat([pd.read_csv(f) for f in glob.glob("data/quali_results_*.csv")], ignore_index=True)

combined_df = pd.merge(
    race_df,
    quali_df,
    on=['Year', 'Round', 'Abbreviation'],
    suffixes=("_race", "_quali")
)

combined_df.to_csv("data/combined_data.csv", index=False)

print("Combined dataset shape:", combined_df.shape)
print(combined_df.head())

# TODO run this and combine