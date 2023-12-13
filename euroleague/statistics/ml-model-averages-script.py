import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import pickle

# columns_needed = ['ROUND','DATE', 'TM NAME', 'OPP NAME','H/A', 'W/L','PTS','2PTM','2PTA','2PT%','3PTM','3PTA','3PT%','FGM','FGA','FG%','FTM','FTA','FT%']

file_path = r'C:\Modesto\PythonKursai\Baigiamasis2\code-academy-baigiamasis\euroleague\statistics\Teams stats.xlsx'
teams_gbg_df = pd.read_excel(file_path, sheet_name='TEAMS_GbG', header=2)
columns_needed = ['TM NAME', 'OPP NAME','H/A', 'W/L','PTS','2PTM','AST','ST','BLK','TR','VAL']

df = teams_gbg_df[columns_needed]

transformed_data = []

for i in range(0, len(df), 2):
    row1 = df.iloc[i]
    row2 = df.iloc[i + 1]

    # Determine which row is for the home team and which is for the away team
    if row1['H/A'] == 'H':
        home_row = row1
        away_row = row2
    else:
        home_row = row2
        away_row = row1

    combined_row = {
        "ROUND" : home_row["ROUND"],
        "TM NAME": home_row["TM NAME"],
        "OPP NAME": away_row["TM NAME"],
        "W/L": home_row["W/L"],
        "PTS_home": home_row["PTS"],
        "PTS_away": away_row["PTS"],
        "2PTM_home": home_row["2PTM"],
        "2PTM_away": away_row["2PTM"],
        "AST_home":home_row["AST"],
        "AST_away":away_row["AST"],
        "ST_home":home_row["ST"],
        "ST_away":away_row["ST"],
        "BLK_home":home_row["BLK"],
        "BLK_away":away_row["BLK"],
        "TR_home":home_row["TR"],
        "TR_away":away_row["TR"],
        "PIR_home":home_row["VAL"],
        "PIR_away":away_row["VAL"]
    }

    transformed_data.append(combined_row)
transformed_df = pd.DataFrame(transformed_data)


transformed_df['W/L']=(transformed_df['W/L'] == 'W').astype("int")


le = LabelEncoder()
le.fit(df["TM NAME"])
transformed_df['tm_code'] = le.transform(transformed_df["TM NAME"])
transformed_df['opp_code'] = le.transform(transformed_df["OPP NAME"])



X=transformed_df[['tm_code','opp_code','PTS_home','PTS_away','2PTM_home','2PTM_away','AST_home','AST_away','ST_home','ST_away','BLK_home','BLK_away','TR_home','TR_away','PIR_home','PIR_away']]
y = transformed_df[['W/L']]
rf = RandomForestClassifier(n_estimators=50, min_samples_split=10, random_state=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

rf.fit(X_train, y_train)

y_trained_pred = rf.predict(X_train)



# for pred, true_pred in zip(y_trained_pred, y_train['W/L'].to_list()):
#     print(pred, true_pred)


# print(f"{rf.score(X_train,y_train)} Train")
# print(f"{rf.score(X_test,y_test)} Test ")



def calculate_team_avg(transformed_df):
    # Get unique team codes and names
    unique_teams = transformed_df[['tm_code', 'TM NAME']].drop_duplicates()

    # List to store the results
    team_stats_data = []

    # Iterate through each team
    for _, row in unique_teams.iterrows():
        team_code = row['tm_code']
        team_name = row['TM NAME']

        # Initialize variables to calculate totals
        home_games = away_games = home_AST = away_AST = home_ST = away_ST = home_BLK = away_BLK = home_TR = away_TR = home_PIR = away_PIR = home_PTS = away_PTS = home_2PTM = away_2PTM = 0

        # Filter DataFrame for the current team as home and away team
        home_df = transformed_df[transformed_df['tm_code'] == team_code]
        away_df = transformed_df[transformed_df['opp_code'] == team_code]

        # Sum home and away stats
        if not home_df.empty:
            home_games = len(home_df)
            home_AST = home_df['AST_home'].sum()
            home_ST = home_df['ST_home'].sum()
            home_BLK = home_df['BLK_home'].sum()
            home_TR = home_df['TR_home'].sum()
            home_PIR = home_df['PIR_home'].sum()
            home_PTS = home_df['PTS_home'].sum()
            home_2PTM = home_df['2PTM_home'].sum()

        if not away_df.empty:
            away_games = len(away_df)
            away_AST = away_df['AST_away'].sum()
            away_ST = away_df['ST_away'].sum()
            away_BLK = away_df['BLK_away'].sum()
            away_TR = away_df['TR_away'].sum()
            away_PIR = away_df['PIR_away'].sum()
            away_PTS = away_df['PTS_away'].sum()
            away_2PTM = away_df['2PTM_away'].sum()

        # Calculate totals
        total_games = home_games + away_games
        if total_games > 0:
            average_AST = (home_AST + away_AST) / total_games
            average_ST = (home_ST + away_ST) / total_games
            average_BLK = (home_BLK + away_BLK) / total_games
            average_TR = (home_TR + away_TR) / total_games
            average_PIR = (home_PIR + away_PIR) / total_games
            average_PTS = (home_PTS + away_PTS) / total_games
            average_2PTM = (home_2PTM + away_2PTM) / total_games
        else:
            average_AST = average_ST = average_BLK = average_TR = average_PIR = average_PTS = average_2PTM = 0

        # Append results to the list
        team_stats_data.append({
            'TM NAME': team_name,
            'tm_code': team_code,
            'Average PTS': average_PTS,
            'Average 2PTM': average_2PTM,
            'Average AST': average_AST,
            'Average ST': average_ST,
            'Average BLK': average_BLK,
            'Average TR': average_TR,
            'Average PIR': average_PIR,
        })

    # Create a DataFrame from the list
    team_stats = pd.DataFrame(team_stats_data)
    return team_stats

averages_df = calculate_team_avg(transformed_df=transformed_df)

# averages_df.to_csv(r"C:\Modesto\PythonKursai\Baigiamasis2\code-academy-baigiamasis\euroleague\statistics\averages_df.csv", index=False)


# Example: Predicting a match between ALBA Berlin (tm_code = 0) and AS Monaco (tm_code = 1)

# Extracting statistics for both teams
# team_A_stats = averages_df[averages_df['tm_code'] == 0]
# team_B_stats = averages_df[averages_df['tm_code'] == 1]


# input_data = [
#     [
#         0,  # tm_code for ALBA Berlin
#         1,  # tm_code for AS Monaco
#         # Assuming ALBA Berlin is playing at home and AS Monaco is away
#         0,  # Home for ALBA Berlin
#         1,  # Away for AS Monaco
#         team_A_stats['Average PTS'].iloc[0],  # Average PTS for ALBA Berlin
#         team_B_stats['Average PTS'].iloc[0],  # Average PTS for AS Monaco
#         team_A_stats['Average 2PTM'].iloc[0],  # 2PTM_home for ALBA Berlin
#         team_B_stats['Average 2PTM'].iloc[0],  # 2PTM_away for AS Monaco
#     ]
# ]

# columns = ['tm_code', 'opp_code', 'H/A_home', 'H/A_away', 'PTS_home', 'PTS_away', '2PTM_home', '2PTM_away']  # Include other column names as per your model
# input_df = pd.DataFrame(input_data, columns=columns)

# # Now you can use this DataFrame for prediction

# predicted_outcome = rf.predict(input_df)
# print("Predicted Outcome:", "Win for ALBA Berlin" if predicted_outcome[0] == 1 else "Lose for ALBA Berlin")




# filename = "predict_win.pkl"  # It's common to use .pkl as the file extension for pickle files
# # Assuming 'model' is your trained model
# pickle.dump(rf, open(filename, 'wb'))  # 'wb' indicates writing in binary mode