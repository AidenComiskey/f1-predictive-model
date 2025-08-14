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

# functiion to get results from qualifying from specified year and round
def get_quali_results(year, round_num):
    quali = ff.get_session(year, round_num, 'Qualifying')
    quali.load()
    quali_results = quali.results[['Position', 'Abbreviation', 'DriverNumber', 'TeamName']].copy()

    quali_results['Year'] = year
    quali_results['Round'] = round_num
    quali_results['Circuit'] = quali.event.Location

    return quali_results

# function that gets data from all sessions from 2018-2025s latest round
def get_all_data(start_year, end_year):
    race_data = []
    quali_data = []

    # loop through the years specified (range is exclusive) and get the schedule for each year
    # number of rounds is different for different years
    for year in range(start_year, end_year + 1):
        schedule = ff.get_event_schedule(year)

        # iterate through each event in the schedule and check if the event has been or not
        for _, event in schedule.iterrows():
            if event['EventDate'] > pd.Timestamp.today():
                continue
            
            # skip over pre season testing
            if 'Testing' in event['EventName']:
                continue
            # get the quali and race results for the event and then add to the lists
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

            # turn the lists into dataframes
            race_df = pd.concat(race_data, ignore_index=True)
            quali_df = pd.concat(quali_data, ignore_index=True)

    return race_df, quali_df

    
#df = get_race_results(2023, 1)
#print(df)
#df = get_quali_results(2025, 1)
#print(df)
race_df, quali_df = get_all_data(2024,2024)
#print(race_df.head())
#print(quali_df.head())
print(race_df.groupby('Year')['Round'].nunique())

# Count how many drivers per race
print(race_df.groupby(['Year', 'Round']).size())