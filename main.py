import pandas as pd
import fastf1 as ff

# cache to store the data fetched from the API
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
