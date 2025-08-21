import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

df = pd.read_csv("data/basic_combined_data_clean.csv")

# create label encoders to convert the data into numbers for the model to use
le_driver = LabelEncoder()
le_team = LabelEncoder()
le_circuit = LabelEncoder()

# convert drivers abbreviation, team name and circuit name to numbers
df['Driver_to_num'] = le_driver.fit_transform(df['Abbreviation'])
df['Team_to_num'] = le_team.fit_transform(df['TeamName_race'])
df['Circuit_to_num'] = le_circuit.fit_transform(df['Circuit_race'])

# set up what will be used to predict and what will be predicted
X = df[['Position_quali', 'GridPosition', 'Driver_to_num', 'Team_to_num', 'Circuit_to_num', 'Year']]
y = df['Position_race']

# split the model into test and train data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# build the model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)