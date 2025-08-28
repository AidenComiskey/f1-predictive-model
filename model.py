import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error

df = pd.read_csv("enhanced_data/combined_data_clean.csv")

# set up what will be used to predict and what will be predicted
X = df[
    ['Position_quali', 'GridPosition', 'Abbreviation', 'TeamName_race', 'Circuit_race','IsWetRace',
     'IsWetQuali', 'BestLap_Sec', 'Year']]
y = df['Position_race']


# categorical features to be converted
cat_features = ['Abbreviation', 'TeamName_race', 'Circuit_race']
encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)

X_encoded = pd.DataFrame(
    encoder.fit_transform(X[cat_features]),
    index=X.index
)

# keep the numeric columns and join them back with the encoded values
X_numeric = X.drop(columns=cat_features)
X_final = pd.concat([X_numeric, X_encoded], axis=1)

# split the model into test and train data
X_train, X_test, y_train, y_test = train_test_split(X_final, y, test_size=0.2, random_state=42)

# build the model
model = XGBRegressor(
    n_estimators=500,
    learning_rate=0.05,
    max_depth=6,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42
)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
print(f"MAE: {mae}")