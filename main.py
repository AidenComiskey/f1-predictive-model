import pandas as pd
import fastf1 as ff

ff.Cache.enable_cache('f1_cache')

def get_race_and_quali(year, round_num):
    race = ff.get_session(year, round_num, 'Race')
    race.load()
    race_results = race.results[['Position', 'Abbreviation', 'DriverNumber', 'TeamName', 'GridPosition']].copy()

    race_results['Year'] = year
    race_results['Round'] = round_num
    race_results['Circuit'] = race.event.Location
    
    return race_results

df = get_race_and_quali(2023, 1)
print(df)