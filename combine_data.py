import pandas as pd
import glob

#combine all years into two dataframes for all race results and all quali results

race_df = pd.concat([pd.read_csv(f) for f in glob.glob("data/race_results_*.csv")], ignore_index=True)
quali_df = pd.concat([pd.read_csv(f) for f in glob.glob("data/quali_results_*.csv")], ignore_index=True)