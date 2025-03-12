# player radar comparison

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from soccerplots.radar_chart import Radar
import streamlit as st



###### Provide data #####
# read in data
standard = pd.read_csv("standard.csv")
shooting = pd.read_csv("shooting.csv")
passing = pd.read_csv("passing.csv")
sca = pd.read_csv("sca.csv")
defensive = pd.read_csv("defensive.csv")

# clean data function
def data_clean(df):
    
    # convert the data into dataframe
    df = pd.DataFrame(df)

    # filter for bundesliga 
    df[['an', 'comp']] = df['Comp'].str.split(' ', n=1, expand=True)
    df = df.drop(columns=['an', 'Comp'])
    df = df[df['Player'] != 'Player']
    df = df[df['comp'] == 'Bundesliga']
    df = df[df['Pos'] != "GK"]
    
    # drop unnecessary columns
    df = df.drop(['Rk', 'Nation', 'Pos', 'comp', 'Squad', 'Age', 'Born', 'Matches'], axis=1)

    return df


# apply function to the collected datasets
standard_df = data_clean(standard)
shooting_df = data_clean(shooting)
passing_df = data_clean(passing)
sca_df = data_clean(sca)
defensive_df = data_clean(defensive)

# select the columns we want to use for the radars
standard_df = standard_df[['Player', 'Gls', 'Ast', 'xG', 'xAG', 'PrgC', 'PrgP', 'PrgR', 'Gls.1', 'Ast.1']]
shooting_df = shooting_df[["Player", 'SoT', 'SoT%', 'G/SoT', 'SoT/90']]
passing_df = passing_df[['Player', 'Cmp', 'Cmp%', 'xA', 'KP', 'PPA', 'CrsPA']]
sca_df = sca_df[["Player", 'SCA', 'SCA90', 'GCA', 'GCA90']]
defensive_df = defensive_df[["Player", 'Tkl', 'TklW', 'Sh', 'Pass', 'Int']]

# combine all the tables together
all_data = pd.merge(standard_df, shooting_df, on="Player")
all_data = pd.merge(all_data, passing_df, on="Player")
all_data = pd.merge(all_data, sca_df, on="Player")
all_data = pd.merge(all_data, defensive_df, on="Player")

# fill all columns with na with 0
all_data = all_data.fillna(0)

# need to fix something on the repetitive joining #######
all_data

# min max the data so every metric is measured out of 100% vs league best
metrics = all_data.iloc[:, 1:]
scaler = MinMaxScaler()
# transform to a dataframe 
data_minmax = pd.DataFrame(scaler.fit_transform(metrics), columns=metrics.columns)
data_minmax

# merge the data back together 
players = all_data['Player']

df = pd.merge(players, data_minmax, left_index=True, right_index=True)
df



# create the next steps where selection by the inputs decides what metrics to compare






#### producing page ####
st.header("Bundesliga 2023-24: Player Comparison Radars")




