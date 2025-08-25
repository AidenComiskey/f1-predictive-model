import pandas as pd
import fastf1 as ff
from fastf1.utils import to_timedelta


# cache to store the data fetched from the API
ff.Cache.enable_cache('f1_cache')

# function to get results from race from specified year and round
def get_race_results(year, round_num):
    race = ff.get_session(year, round_num, 'Race')
    race.load()
    race_results = race.results[['Position', 'Abbreviation', 'DriverNumber', 'TeamName', 'GridPosition', 'Status', 'Time']].copy()

    # create a column for the race time in seconds and convert time column to seconds
    race_results['RaceTime_Sec'] = race_results['Time'].apply(lambda x: to_timedelta(x).total_seconds() if pd.notna(x) else None)

    # get all valid pit stops from the race and add it to pitstops column
    # fill null values with 0 to indicate no pit stops
    pitstops = race.laps.groupby('DriverNumber').apply(lambda x: (x['PitInTime'].notna() & x['PitOutTime'].notna()).sum())
    race_results['PitStops'] = race_results['DriverNumber'].map(pitstops).fillna(0).astype(int)

    # check if it was a wet race, true if rainfall is > 0mm
    is_wet = race.weather_data['Rainfall'].sum() > 0
    race_results['IsWetRace'] = int(is_wet)

    race_results['Year'] = year
    race_results['Round'] = round_num
    race_results['Circuit'] = race.event.Location

    race_results.drop(columns=['Time'], inplace = True)
    
    return race_results

# function to get results from qualifying from specified year and round
def get_quali_results(year, round_num):
    quali = ff.get_session(year, round_num, 'Qualifying')
    quali.load()
    quali_results = quali.results[['Position', 'Abbreviation', 'DriverNumber', 'TeamName']].copy()

    # get every drivers fastest lap of qualifying
    laps = quali.laps
    fastest_laps = (
        laps.groupby("DriverNumber")
        .apply(lambda x: x.pick_fastest())
        .reset_index(drop=True)
    )

    # turn the fastest lap times into seconds
    fastest_laps['BestLap_Sec'] = fastest_laps['LapTime'].dt.total_seconds()

    # merge the current quali results dataframe with the fastest laps dataframe
    quali_results = quali_results.merge(
        fastest_laps[['DriverNumber','BestLap_Sec']],
        on='DriverNumber',
        how='left'
    )

    # add if it was a wet qualifying into the dataframe
    is_wet = quali.weather_data['Rainfall'].sum() > 0
    quali_results['IsWetQuali'] = int(is_wet)

    quali_results['Year'] = year
    quali_results['Round'] = round_num
    quali_results['Circuit'] = quali.event.Location

    return quali_results

# function to get quali and race data for a specified year using the helper functions
def get_year_data(year):
    race_data = []
    quali_data = []

    # if any issues encountered fetching from API then catch the exception
    try:
        schedule = ff.get_event_schedule(year)
    except Exception as e:
        print(f"Skipping {year} due to error: {e}")
        return None, None

    # iterate through each event and stop if the race weekend has not been yet
    # also check to see if it is a testing event and ignore if so
    for _, event in schedule.iterrows():
        if event['EventDate'] > pd.Timestamp.today():
            continue
        if 'Testing' in event['EventName']:
            continue

        round_num = event['RoundNumber']
        
        # use helper functions to get data for each session
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
    # store every session from the year as one big dataframe
    race_df = pd.concat(race_data, ignore_index=True) if race_data else None
    quali_df = pd.concat(quali_data, ignore_index=True) if quali_data else None

    return race_df, quali_df
