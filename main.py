import pandas as pd
import fastf1 as ff

ff.Cache.enable_cache('f1_cache')

# function to get results from race from specified year and round
def get_race_results(year, round_num):
    race = ff.get_session(year, round_num, 'Race')
    race.load()
    race_results = race.results[['Position', 'Abbreviation', 'DriverNumber', 'TeamName', 'GridPosition']].copy()

    race_results['Year'] = year
    race_results['Round'] = round_num
    race_results['Circuit'] = race.event.Location
    
    return race_results

# function to get results from qualifying from specified year and round
def get_quali_results(year, round_num):
    quali = ff.get_session(year, round_num, 'Qualifying')
    quali.load()
    quali_results = quali.results[['Position', 'Abbreviation', 'DriverNumber', 'TeamName']].copy()

    quali_results['Year'] = year
    quali_results['Round'] = round_num
    quali_results['Circuit'] = quali.event.Location

    return quali_results

# function to get quali and race data for a specified year using the helper functions
def get_year_data(year):
    race_data = []
    quali_data = []

    try:
        schedule = ff.get_event_schedule(year)
    except Exception as e:
        print(f"Skipping {year} due to error: {e}")
        return None, None

    for _, event in schedule.iterrows():
        if event['EventDate'] > pd.Timestamp.today():
            continue
        if 'Testing' in event['EventName']:
            continue

        round_num = event['RoundNumber']

        try:
            quali_result = get_quali_results(year, round_num)
            quali_data.append(quali_result)
        except Exception as e:
            print(f"Skipping quali {event['EventName']} ({year}) due to error: {e}")

        try:
            race_result = get_race_results(year, round_num)
            race_data.append(race_result)
        except Exception as e:
            print(f"Skipping race {event['EventName']} ({year}) due to error: {e}")

    race_df = pd.concat(race_data, ignore_index=True) if race_data else None
    quali_df = pd.concat(quali_data, ignore_index=True) if quali_data else None

    return race_df, quali_df


for year in range(2018, 2026):  # up to 2025
    try:
        race_df, quali_df = get_year_data(year)  # should load from cache
        race_df.to_csv(f"race_results_{year}.csv", index=False)
        quali_df.to_csv(f"quali_results_{year}.csv", index=False)
        print(f"Saved {year} data to CSV")
    except Exception as e:
        print(f"Skipping {year} due to error: {e}")

        