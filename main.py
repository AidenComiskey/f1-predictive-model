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

#df = get_race_results(2023, 1)
#print(df)
df = get_quali_results(2023, 1)
print(df)