from main import get_year_data

# use to load all data for qualifying and race sessions from 2018 to as of the last race weekend occurred
# saves data into a separate csv for race and quali for each year
for year in range(2018, 2026):  # up to 2025
    try:
        race_df, quali_df = get_year_data(year)  # should load from cache
        race_df.to_csv(f"race_results_{year}.csv", index=False)
        quali_df.to_csv(f"quali_results_{year}.csv", index=False)
        print(f"Saved {year} data to CSV")
    except Exception as e:
        print(f"Skipping {year} due to error: {e}")