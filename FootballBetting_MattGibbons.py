# Assessing the data

# Import libraries
import pandas as pd
import numpy as np
import sqlite3
import matplotlib.pyplot as plt
% matplotlib inline

# Extract the League table

# Create connection to SQLite database
conn = sqlite3.connect('database.sqlite')

# Create a dataframe of all data from the League table using pandas to interface with SQLite
df_assess_league = pd.read_sql("SELECT * From League", conn)

# Close the database connection
conn.close()
df_assess_league

# Extract the Team table and check the first and last few rows

conn = sqlite3.connect('database.sqlite')
df_assess_team = pd.read_sql("SELECT * From Team", conn)
conn.close()
df_assess_team.head(2)

df_assess_team.tail(2)

# Check type and data counts

df_assess_team.info()

# Check unique values

df_assess_team.nunique()

# Extract the Match table and check first and last rows

conn = sqlite3.connect('database.sqlite')
df_assess_match = pd.read_sql("SELECT l.name, m.* From Match m LEFT JOIN League l ON m.league_id = l.id ", conn)
conn.close()
df_assess_match.head(2)

df_assess_match.tail(2)

# Check the number of rows and columns in the table

df_assess_match.shape

# Check data types

df_assess_match.dtypes

# Some columns are missing above but we can pull the complete by using

for i, v in enumerate(df_assess_match.columns):
    print(i, v)

# Count of match per league
df_assess_match['name'].value_counts()



# Pie chart of count of matches per league
df_assess_match['name'].value_counts().plot(kind='pie', figsize=(8, 8));

# Let's look in more detail at the columns we'll be using

conn = sqlite3.connect('database.sqlite')
df_assess_match2 = pd.read_sql("SELECT B365H, B365D, B365A, BWH, BWD, BWA, IWH, IWD, IWA, LBH, LBD, LBA, PSH, PSD, PSA, WHH, WHD, WHA, SJH, SJD, SJA, VCH, VCD, VCA, GBH, GBD, GBA, BSH, BSD, BSA From Match", conn)
conn.close()
df_assess_match2.describe()

# Bookmaker home win odds by league

conn = sqlite3.connect('database.sqlite')
df_assess_match3 = pd.read_sql("SELECT l.name, AVG(m.B365H) B365H, AVG(m.BWH) BWH, AVG(m.IWH) IWH, AVG(m.LBH) LBH, AVG(m.PSH) PSH, AVG(m.WHH) WHH, AVG(m.SJH) SJH, AVG(m.VCH) VCH, AVG(m.GBH) GBH, AVG(m.BSA) BSA FROM Match m LEFT JOIN League l ON m.league_id = l.id GROUP BY 1", conn)
conn.close()
df_assess_match3

# Bookmaker home win odds by season

conn = sqlite3.connect('database.sqlite')
df_assess_match4 = pd.read_sql("SELECT Season, AVG(B365H), AVG(BWH), AVG(IWH), AVG(LBH), AVG(PSH), AVG(WHH), AVG(SJH), AVG(VCH), AVG(GBH), AVG(BSH) From Match GROUP BY 1", conn)
conn.close()
df_assess_match4



# Exploring data - the odds for a home win

# Create dataframes for home and away odds

conn = sqlite3.connect('database.sqlite')
df_b365h = pd.read_sql("SELECT B365H FROM Match", conn)
df_b365a = pd.read_sql("SELECT B365A FROM Match", conn)
conn.close()

# Plot the dataframes on the same histogram

fig, ax = plt.subplots(figsize=(8, 6))
ax.hist(df_b365h['B365H'].dropna(), alpha=0.5, label='B365H')
ax.hist(df_b365a['B365A'].dropna(), alpha=0.5, label='B365A')
ax.set_title('Odds for home and away wins')
ax.set_xlabel('Odds')
ax.set_ylabel('Freq')
ax.legend(loc='upper right')
plt.show()

# Create dataframes for home and away odds, for Manchester United

conn = sqlite3.connect('database.sqlite')
df_b365h_manu = pd.read_sql("SELECT t1.team_long_name home_team, t2.team_long_name away_team, m.B365H FROM Match m LEFT JOIN Team t1 ON m.home_team_api_id = t1.team_api_id LEFT JOIN Team t2 ON m.away_team_api_id = t2.team_api_id WHERE t1.team_long_name = 'Manchester United'", conn)
df_b365a_manu = pd.read_sql("SELECT t1.team_long_name home_team, t2.team_long_name away_team, m.B365A FROM Match m LEFT JOIN Team t1 ON m.home_team_api_id = t1.team_api_id LEFT JOIN Team t2 ON m.away_team_api_id = t2.team_api_id WHERE t2.team_long_name = 'Manchester United'", conn)
conn.close()

# Plot the dataframes on the same histogram

fig, ax = plt.subplots(figsize=(8, 6))
ax.hist(df_b365h_manu['B365H'], alpha=0.5, label='B365H')
ax.hist(df_b365a_manu['B365A'], alpha=0.5, label='B365A')
ax.set_title('Sample of odds for Manchester United to win home and away')
ax.set_xlabel('Odds')
ax.set_ylabel('Freq')
ax.legend(loc='upper right')
plt.show()

# Create dataframes for home and away odds, for FC Barcelona

conn = sqlite3.connect('database.sqlite')
df_b365h_manu = pd.read_sql("SELECT t1.team_long_name home_team, t2.team_long_name away_team, m.B365H FROM Match m LEFT JOIN Team t1 ON m.home_team_api_id = t1.team_api_id LEFT JOIN Team t2 ON m.away_team_api_id = t2.team_api_id WHERE t1.team_long_name = 'FC Barcelona'", conn)
df_b365a_manu = pd.read_sql("SELECT t1.team_long_name home_team, t2.team_long_name away_team, m.B365A FROM Match m LEFT JOIN Team t1 ON m.home_team_api_id = t1.team_api_id LEFT JOIN Team t2 ON m.away_team_api_id = t2.team_api_id WHERE t2.team_long_name = 'FC Barcelona'", conn)
conn.close()

# Plot the dataframes on the same histogram

fig, ax = plt.subplots(figsize=(8, 6))
ax.hist(df_b365h_manu['B365H'], alpha=0.5, label='B365H')
ax.hist(df_b365a_manu['B365A'], alpha=0.5, label='B365A')
ax.set_title('Sample of odds for FC Barcelona to win home and away')
ax.set_xlabel('Odds')
ax.set_ylabel('Freq')
ax.legend(loc='upper right')
plt.show()



# Exploring data - the implied probabilities per match

# Select the first odds from the list for bookmaker Bet 365

conn = sqlite3.connect('database.sqlite')
df_example_odds = pd.read_sql("SELECT B365H, B365D, B365A FROM Match WHERE id=1", conn)
conn.close()
df_example_odds

# Let's start high level, by calculating the implied odds per match, per bookmaker

# First let's extract from SQL the average of odds per bookmaker split by result

conn = sqlite3.connect('database.sqlite')
df_gam_SQLSQL = pd.read_sql("SELECT AVG(m.B365H) B365H, AVG(m.B365D) B365D, AVG(m.B365A) B365A, AVG(m.BWH) BWH, AVG(m.BWD) BWD, AVG(m.BWA) BWA, AVG(m.IWH) IWH, AVG(m.IWD) IWD, AVG(m.IWA) IWA, AVG(m.LBH) LBH, AVG(m.LBD) LBD, AVG(m.LBA) LBA, AVG(m.PSH) PSH, AVG(m.PSD) PSD, AVG(m.PSA) PSA, AVG(m.WHH) WHH, AVG(m.WHD) WHD, AVG(m.WHA) WHA, AVG(m.SJH) SJH, AVG(m.SJD) SJD, AVG(m.SJA) SJA, AVG(m.VCH) VCH, AVG(m.VCD) VCD, AVG(m.VCA) VCA, AVG(m.GBH) GBH, AVG(m.GBD) GBD, AVG(m.GBA) GBA, AVG(m.BSH) BSH, AVG(m.BSD) BSD, AVG(m.BSA) BSA FROM Match m LEFT JOIN League l ON m.league_id = l.id", conn)
conn.close()
df_gam_SQLSQL

# Then let's convert them to implied probabilities by dividing them into 1

df_gam_SQLSQL_1fun = df_gam_SQLSQL.applymap(lambda x: 1/x)
df_gam_SQLSQL_1fun

# Finally let's cobmine the 3 possible results to match level

df_gam_SQLSQL_1fun_con = pd.DataFrame()
df_gam_SQLSQL_1fun_con['B365'] = df_gam_SQLSQL_1fun['B365H'] + df_gam_SQLSQL_1fun['B365D'] + df_gam_SQLSQL_1fun['B365A']
df_gam_SQLSQL_1fun_con['BW'] = df_gam_SQLSQL_1fun['BWH'] + df_gam_SQLSQL_1fun['BWD'] + df_gam_SQLSQL_1fun['BWA']
df_gam_SQLSQL_1fun_con['IW'] = df_gam_SQLSQL_1fun['IWH'] + df_gam_SQLSQL_1fun['IWD'] + df_gam_SQLSQL_1fun['IWA']
df_gam_SQLSQL_1fun_con['LB'] = df_gam_SQLSQL_1fun['LBH'] + df_gam_SQLSQL_1fun['LBD'] + df_gam_SQLSQL_1fun['LBA']
df_gam_SQLSQL_1fun_con['PS'] = df_gam_SQLSQL_1fun['PSH'] + df_gam_SQLSQL_1fun['PSD'] + df_gam_SQLSQL_1fun['PSA']
df_gam_SQLSQL_1fun_con['WH'] = df_gam_SQLSQL_1fun['WHH'] + df_gam_SQLSQL_1fun['WHD'] + df_gam_SQLSQL_1fun['WHA']
df_gam_SQLSQL_1fun_con['SJ'] = df_gam_SQLSQL_1fun['SJH'] + df_gam_SQLSQL_1fun['SJD'] + df_gam_SQLSQL_1fun['SJA']
df_gam_SQLSQL_1fun_con['VC'] = df_gam_SQLSQL_1fun['VCH'] + df_gam_SQLSQL_1fun['VCD'] + df_gam_SQLSQL_1fun['VCA']
df_gam_SQLSQL_1fun_con['GB'] = df_gam_SQLSQL_1fun['GBH'] + df_gam_SQLSQL_1fun['GBD'] + df_gam_SQLSQL_1fun['GBA']
df_gam_SQLSQL_1fun_con['BS'] = df_gam_SQLSQL_1fun['BSH'] + df_gam_SQLSQL_1fun['BSD'] + df_gam_SQLSQL_1fun['BSA']
df_gam_SQLSQL_1fun_con

# Implied probabilities per bookmaker, by season

# First let's extract from SQL the average of odds per bookmaker split by result, this time grouped by season

conn = sqlite3.connect('database.sqlite')
df_gam_SQLSQL_s = pd.read_sql("SELECT m.season, AVG(m.B365H) B365H, AVG(m.B365D) B365D, AVG(m.B365A) B365A, AVG(m.BWH) BWH, AVG(m.BWD) BWD, AVG(m.BWA) BWA, AVG(m.IWH) IWH, AVG(m.IWD) IWD, AVG(m.IWA) IWA, AVG(m.LBH) LBH, AVG(m.LBD) LBD, AVG(m.LBA) LBA, AVG(m.PSH) PSH, AVG(m.PSD) PSD, AVG(m.PSA) PSA, AVG(m.WHH) WHH, AVG(m.WHD) WHD, AVG(m.WHA) WHA, AVG(m.SJH) SJH, AVG(m.SJD) SJD, AVG(m.SJA) SJA, AVG(m.VCH) VCH, AVG(m.VCD) VCD, AVG(m.VCA) VCA, AVG(m.GBH) GBH, AVG(m.GBD) GBD, AVG(m.GBA) GBA, AVG(m.BSH) BSH, AVG(m.BSD) BSD, AVG(m.BSA) BSA FROM Match m LEFT JOIN League l ON m.league_id = l.id GROUP BY 1", conn)
conn.close()
df_gam_SQLSQL_s

# Then let's convert them to implied probabilities by dividing them into 1

df_1 = pd.DataFrame()
df_1['season'] = df_gam_SQLSQL_s['season']
df_2 = df_gam_SQLSQL_s.iloc[:,1:].applymap(lambda x: 1/x)
df_gam_SQLSQL_s_1fun = pd.concat([df_1, df_2], axis=1)
df_gam_SQLSQL_s_1fun

# Finally let's cobmine the 3 possible results to match level

df_gam_SQLSQL_s_1fun_con = pd.DataFrame()
df_gam_SQLSQL_s_1fun_con['Season'] = df_gam_SQLSQL_s_1fun['season']
df_gam_SQLSQL_s_1fun_con['B365'] = df_gam_SQLSQL_s_1fun['B365H'] + df_gam_SQLSQL_s_1fun['B365D'] + df_gam_SQLSQL_s_1fun['B365A']
df_gam_SQLSQL_s_1fun_con['BW'] = df_gam_SQLSQL_s_1fun['BWH'] + df_gam_SQLSQL_s_1fun['BWD'] + df_gam_SQLSQL_s_1fun['BWA']
df_gam_SQLSQL_s_1fun_con['IW'] = df_gam_SQLSQL_s_1fun['IWH'] + df_gam_SQLSQL_s_1fun['IWD'] + df_gam_SQLSQL_s_1fun['IWA']
df_gam_SQLSQL_s_1fun_con['LB'] = df_gam_SQLSQL_s_1fun['LBH'] + df_gam_SQLSQL_s_1fun['LBD'] + df_gam_SQLSQL_s_1fun['LBA']
df_gam_SQLSQL_s_1fun_con['PS'] = df_gam_SQLSQL_s_1fun['PSH'] + df_gam_SQLSQL_s_1fun['PSD'] + df_gam_SQLSQL_s_1fun['PSA']
df_gam_SQLSQL_s_1fun_con['WH'] = df_gam_SQLSQL_s_1fun['WHH'] + df_gam_SQLSQL_s_1fun['WHD'] + df_gam_SQLSQL_s_1fun['WHA']
df_gam_SQLSQL_s_1fun_con['SJ'] = df_gam_SQLSQL_s_1fun['SJH'] + df_gam_SQLSQL_s_1fun['SJD'] + df_gam_SQLSQL_s_1fun['SJA']
df_gam_SQLSQL_s_1fun_con['VC'] = df_gam_SQLSQL_s_1fun['VCH'] + df_gam_SQLSQL_s_1fun['VCD'] + df_gam_SQLSQL_s_1fun['VCA']
df_gam_SQLSQL_s_1fun_con['GB'] = df_gam_SQLSQL_s_1fun['GBH'] + df_gam_SQLSQL_s_1fun['GBD'] + df_gam_SQLSQL_s_1fun['GBA']
df_gam_SQLSQL_s_1fun_con['BS'] = df_gam_SQLSQL_s_1fun['BSH'] + df_gam_SQLSQL_s_1fun['BSD'] + df_gam_SQLSQL_s_1fun['BSA']
df_gam_SQLSQL_s_1fun_con

# Plot match level implied probabilities per bookmaker over time

df_gam_SQLSQL_s_1fun_con.plot(x="Season", y=["B365", "BW", "IW", "LB", "PS", "WH", "SJ", "VC", "GB", "BS"], kind="line", figsize=(8, 8))

# Add titles
plt.title("Implied match level probabilities, 2008 to 2016", loc='left', fontsize=12, fontweight=0, color='black')
plt.ylabel("Implied probabilities");

# Implied match level probabilities per bookmaker, by league

# First let's extract from SQL the average of odds per bookmaker split by result, this time grouped by league name

conn = sqlite3.connect('database.sqlite')
df_gam_SQLSQL_l = pd.read_sql("SELECT l.name, AVG(m.B365H) B365H, AVG(m.B365D) B365D, AVG(m.B365A) B365A, AVG(m.BWH) BWH, AVG(m.BWD) BWD, AVG(m.BWA) BWA, AVG(m.IWH) IWH, AVG(m.IWD) IWD, AVG(m.IWA) IWA, AVG(m.LBH) LBH, AVG(m.LBD) LBD, AVG(m.LBA) LBA, AVG(m.PSH) PSH, AVG(m.PSD) PSD, AVG(m.PSA) PSA, AVG(m.WHH) WHH, AVG(m.WHD) WHD, AVG(m.WHA) WHA, AVG(m.SJH) SJH, AVG(m.SJD) SJD, AVG(m.SJA) SJA, AVG(m.VCH) VCH, AVG(m.VCD) VCD, AVG(m.VCA) VCA, AVG(m.GBH) GBH, AVG(m.GBD) GBD, AVG(m.GBA) GBA, AVG(m.BSH) BSH, AVG(m.BSD) BSD, AVG(m.BSA) BSA FROM Match m LEFT JOIN League l ON m.league_id = l.id GROUP BY 1", conn)
conn.close()
df_gam_SQLSQL_l

# Then let's convert them to implied probabilities by dividing them into 1

df_1 = pd.DataFrame()
df_1['name'] = df_gam_SQLSQL_l['name']
df_2 = df_gam_SQLSQL_l.iloc[:,1:].applymap(lambda x: 1/x)
df_gam_SQLSQL_l_1fun = pd.concat([df_1, df_2], axis=1)
df_gam_SQLSQL_l_1fun

# Next let's cobmine the 3 possible results to match level

df_gam_SQLSQL_l_1fun_con = pd.DataFrame()
df_gam_SQLSQL_l_1fun_con['League'] = df_gam_SQLSQL_l_1fun['name']
df_gam_SQLSQL_l_1fun_con['B365'] = df_gam_SQLSQL_l_1fun['B365H'] + df_gam_SQLSQL_l_1fun['B365D'] + df_gam_SQLSQL_l_1fun['B365A']
df_gam_SQLSQL_l_1fun_con['BW'] = df_gam_SQLSQL_l_1fun['BWH'] + df_gam_SQLSQL_l_1fun['BWD'] + df_gam_SQLSQL_l_1fun['BWA']
df_gam_SQLSQL_l_1fun_con['IW'] = df_gam_SQLSQL_l_1fun['IWH'] + df_gam_SQLSQL_l_1fun['IWD'] + df_gam_SQLSQL_l_1fun['IWA']
df_gam_SQLSQL_l_1fun_con['LB'] = df_gam_SQLSQL_l_1fun['LBH'] + df_gam_SQLSQL_l_1fun['LBD'] + df_gam_SQLSQL_l_1fun['LBA']
df_gam_SQLSQL_l_1fun_con['PS'] = df_gam_SQLSQL_l_1fun['PSH'] + df_gam_SQLSQL_l_1fun['PSD'] + df_gam_SQLSQL_l_1fun['PSA']
df_gam_SQLSQL_l_1fun_con['WH'] = df_gam_SQLSQL_l_1fun['WHH'] + df_gam_SQLSQL_l_1fun['WHD'] + df_gam_SQLSQL_l_1fun['WHA']
df_gam_SQLSQL_l_1fun_con['SJ'] = df_gam_SQLSQL_l_1fun['SJH'] + df_gam_SQLSQL_l_1fun['SJD'] + df_gam_SQLSQL_l_1fun['SJA']
df_gam_SQLSQL_l_1fun_con['VC'] = df_gam_SQLSQL_l_1fun['VCH'] + df_gam_SQLSQL_l_1fun['VCD'] + df_gam_SQLSQL_l_1fun['VCA']
df_gam_SQLSQL_l_1fun_con['GB'] = df_gam_SQLSQL_l_1fun['GBH'] + df_gam_SQLSQL_l_1fun['GBD'] + df_gam_SQLSQL_l_1fun['GBA']
df_gam_SQLSQL_l_1fun_con['BS'] = df_gam_SQLSQL_l_1fun['BSH'] + df_gam_SQLSQL_l_1fun['BSD'] + df_gam_SQLSQL_l_1fun['BSA']

# Finally let's highlight max and min values in yellow and orange, respectively

# Functions from https://pandas.pydata.org/pandas-docs/stable/style.html

df_improb_league = df_gam_SQLSQL_l_1fun_con.set_index('League')

def highlight_max(s):
    '''
    highlight max values in yellow.
    '''
    is_max = s == s.max()
    return ['background-color: yellow' if v else '' for v in is_max]

def highlight_min(s):
    '''
    highlight min values in orange
    '''
    is_min = s == s.min()
    return ['background-color: orange' if v else '' for v in is_min]

df_improb_league.style.\
    apply(highlight_min).\
    apply(highlight_max)



# Exploring data - rates of return

# Calculate the odds paid out across all winners by PS

conn = sqlite3.connect('database.sqlite')
df_winning_odds = pd.read_sql("SELECT CASE WHEN home_team_goal > away_team_goal THEN PSH WHEN home_team_goal = away_team_goal THEN PSD ELSE PSA END AS winning_odds FROM Match", conn)
conn.close()
df_winning_odds.describe()

# Calculate the odds paid out across all winners by IW

conn = sqlite3.connect('database.sqlite')
df_risk = pd.read_sql("SELECT CASE WHEN m.home_team_goal > m.away_team_goal THEN m.IWH WHEN m.home_team_goal = m.away_team_goal THEN m.IWD ELSE m.IWA END AS winning_odds FROM Match m", conn)
conn.close()
df_risk.describe()

# Calculate payout rate for match favourite with PS

conn = sqlite3.connect('database.sqlite')
df_favourite_PS = pd.read_sql("SELECT PSH, PSD, PSA, CASE WHEN home_team_goal > away_team_goal AND (PSH <= PSD AND PSH <= PSA) THEN PSH WHEN home_team_goal > away_team_goal AND NOT (PSH <= PSD AND PSH <= PSA) THEN 0 WHEN home_team_goal = away_team_goal AND (PSD < PSH AND PSD < PSA) THEN PSD WHEN home_team_goal = away_team_goal AND NOT (PSD < PSH AND PSD < PSA) THEN 0 WHEN home_team_goal < away_team_goal AND (PSA < PSH AND PSA < PSD) THEN PSA WHEN home_team_goal < away_team_goal AND NOT (PSA < PSH AND PSA < PSD) THEN 0 ELSE null END AS payout FROM Match", conn)
conn.close()
df_favourite_PS.describe()

# Calculate payout rate for match favourite with IW

conn = sqlite3.connect('database.sqlite')
df_favourite_IW = pd.read_sql("SELECT IWH, IWD, IWA, CASE WHEN home_team_goal > away_team_goal AND (IWH <= IWD AND IWH <= IWA) THEN IWH WHEN home_team_goal > away_team_goal AND NOT (IWH <= IWD AND IWH <= IWA) THEN 0 WHEN home_team_goal = away_team_goal AND (IWD < IWH AND IWD < IWA) THEN IWD WHEN home_team_goal = away_team_goal AND NOT (IWD < IWH AND IWD < IWA) THEN 0 WHEN home_team_goal < away_team_goal AND (IWA < IWH AND IWA < IWD) THEN IWA WHEN home_team_goal < away_team_goal AND NOT (IWA < IWH AND IWA < IWD) THEN 0 ELSE null END AS payout FROM Match", conn)
conn.close()
df_favourite_IW.describe()

# Calculate payout rate for 1st, 2nd and 3rd favourites with PS

conn = sqlite3.connect('database.sqlite')
df_favourites_PS = pd.read_sql("SELECT PSH, PSD, PSA, CASE WHEN home_team_goal > away_team_goal AND (PSH <= PSD AND PSH <= PSA) THEN PSH WHEN home_team_goal > away_team_goal AND NOT (PSH <= PSD AND PSH <= PSA) THEN 0 WHEN home_team_goal = away_team_goal AND (PSD <= PSH AND PSD <= PSA) THEN PSD WHEN home_team_goal = away_team_goal AND NOT (PSD <= PSH AND PSD <= PSA) THEN 0 WHEN home_team_goal < away_team_goal AND (PSA <= PSH AND PSA <= PSD) THEN PSA WHEN home_team_goal < away_team_goal AND NOT (PSA <= PSH AND PSA <= PSD) THEN 0 ELSE null END AS pay_fav1, CASE WHEN home_team_goal > away_team_goal AND ((PSH <= PSD AND PSH >= PSA) OR (PSH >= PSD AND PSH <= PSA)) THEN PSH WHEN home_team_goal > away_team_goal AND NOT ((PSH <= PSD AND PSH >= PSA) OR (PSH >= PSD AND PSH <= PSA)) THEN 0 WHEN home_team_goal = away_team_goal AND ((PSD <= PSH AND PSD >= PSA) OR (PSH >= PSD AND PSH <= PSA)) THEN PSD WHEN home_team_goal = away_team_goal AND NOT ((PSD <= PSH AND PSD >= PSA) OR (PSH >= PSD AND PSH <= PSA)) THEN 0 WHEN home_team_goal < away_team_goal AND ((PSA <= PSH AND PSA >= PSD) OR (PSH >= PSD AND PSH <= PSA)) THEN PSA WHEN home_team_goal < away_team_goal AND NOT ((PSA <= PSH AND PSA >= PSD) OR (PSH >= PSD AND PSH <= PSA)) THEN 0 ELSE null END AS pay_fav2, CASE WHEN home_team_goal > away_team_goal AND (PSH >= PSD AND PSH >= PSA) THEN PSH WHEN home_team_goal > away_team_goal AND NOT (PSH >= PSD AND PSH >= PSA) THEN 0 WHEN home_team_goal = away_team_goal AND (PSD >= PSH AND PSD >= PSA) THEN PSD WHEN home_team_goal = away_team_goal AND NOT (PSD >= PSH AND PSD >= PSA) THEN 0 WHEN home_team_goal < away_team_goal AND (PSA >= PSH AND PSA >= PSD) THEN PSA WHEN home_team_goal < away_team_goal AND NOT (PSA >= PSH AND PSA >= PSD) THEN 0 ELSE null END AS pay_fav3 FROM Match", conn)
conn.close()
df_favourites_PS.mean()

# Calculate payout rate for 1st, 2nd and 3rd favourites with IW

conn = sqlite3.connect('database.sqlite')
df_favourites_IW = pd.read_sql("SELECT IWH, IWD, IWA, CASE WHEN home_team_goal > away_team_goal AND (IWH <= IWD AND IWH <= IWA) THEN IWH WHEN home_team_goal > away_team_goal AND NOT (IWH <= IWD AND IWH <= IWA) THEN 0 WHEN home_team_goal = away_team_goal AND (IWD <= IWH AND IWD <= IWA) THEN IWD WHEN home_team_goal = away_team_goal AND NOT (IWD <= IWH AND IWD <= IWA) THEN 0 WHEN home_team_goal < away_team_goal AND (IWA <= IWH AND IWA <= IWD) THEN IWA WHEN home_team_goal < away_team_goal AND NOT (IWA <= IWH AND IWA <= IWD) THEN 0 ELSE null END AS pay_fav1, CASE WHEN home_team_goal > away_team_goal AND ((IWH <= IWD AND IWH >= IWA) OR (IWH >= IWD AND IWH <= IWA)) THEN IWH WHEN home_team_goal > away_team_goal AND NOT ((IWH <= IWD AND IWH >= IWA) OR (IWH >= IWD AND IWH <= IWA)) THEN 0 WHEN home_team_goal = away_team_goal AND ((IWD <= IWH AND IWD >= IWA) OR (IWH >= IWD AND IWH <= IWA)) THEN IWD WHEN home_team_goal = away_team_goal AND NOT ((IWD <= IWH AND IWD >= IWA) OR (IWH >= IWD AND IWH <= IWA)) THEN 0 WHEN home_team_goal < away_team_goal AND ((IWA <= IWH AND IWA >= IWD) OR (IWH >= IWD AND IWH <= IWA)) THEN IWA WHEN home_team_goal < away_team_goal AND NOT ((IWA <= IWH AND IWA >= IWD) OR (IWH >= IWD AND IWH <= IWA)) THEN 0 ELSE null END AS pay_fav2, CASE WHEN home_team_goal > away_team_goal AND (IWH >= IWD AND IWH >= IWA) THEN IWH WHEN home_team_goal > away_team_goal AND NOT (IWH >= IWD AND IWH >= IWA) THEN 0 WHEN home_team_goal = away_team_goal AND (IWD >= IWH AND IWD >= IWA) THEN IWD WHEN home_team_goal = away_team_goal AND NOT (IWD >= IWH AND IWD >= IWA) THEN 0 WHEN home_team_goal < away_team_goal AND (IWA >= IWH AND IWA >= IWD) THEN IWA WHEN home_team_goal < away_team_goal AND NOT (IWA >= IWH AND IWA >= IWD) THEN 0 ELSE null END AS pay_fav3 FROM Match", conn)
conn.close()
df_favourites_IW.mean()

# Calculate payout rate for match favourite for all bookmakers, by league

conn = sqlite3.connect('database.sqlite')
df_favourite_PS_IW_leagues = pd.read_sql("SELECT l.name League, AVG(CASE WHEN home_team_goal > away_team_goal AND (PSH <= PSD AND PSH <= PSA) THEN PSH WHEN home_team_goal > away_team_goal AND NOT (PSH <= PSD AND PSH <= PSA) THEN 0 WHEN home_team_goal = away_team_goal AND (PSD < PSH AND PSD < PSA) THEN PSD WHEN home_team_goal = away_team_goal AND NOT (PSD < PSH AND PSD < PSA) THEN 0 WHEN home_team_goal < away_team_goal AND (PSA < PSH AND PSA < PSD) THEN PSA WHEN home_team_goal < away_team_goal AND NOT (PSA < PSH AND PSA < PSD) THEN 0 ELSE null END) AS payout_PS, AVG(CASE WHEN home_team_goal > away_team_goal AND (IWH <= IWD AND IWH <= IWA) THEN IWH WHEN home_team_goal > away_team_goal AND NOT (IWH <= IWD AND IWH <= IWA) THEN 0 WHEN home_team_goal = away_team_goal AND (IWD < IWH AND IWD < IWA) THEN IWD WHEN home_team_goal = away_team_goal AND NOT (IWD < IWH AND IWD < IWA) THEN 0 WHEN home_team_goal < away_team_goal AND (IWA < IWH AND IWA < IWD) THEN IWA WHEN home_team_goal < away_team_goal AND NOT (IWA < IWH AND IWA < IWD) THEN 0 ELSE null END) AS payout_IW, AVG(CASE WHEN home_team_goal > away_team_goal AND (B365H <= B365D AND B365H <= B365A) THEN B365H WHEN home_team_goal > away_team_goal AND NOT (B365H <= B365D AND B365H <= B365A) THEN 0 WHEN home_team_goal = away_team_goal AND (B365D < B365H AND B365D < B365A) THEN B365D WHEN home_team_goal = away_team_goal AND NOT (B365D < B365H AND B365D < B365A) THEN 0 WHEN home_team_goal < away_team_goal AND (B365A < B365H AND B365A < B365D) THEN B365A WHEN home_team_goal < away_team_goal AND NOT (B365A < B365H AND B365A < B365D) THEN 0 ELSE null END) AS payout_B365, AVG(CASE WHEN home_team_goal > away_team_goal AND (BWH <= BWD AND BWH <= BWA) THEN BWH WHEN home_team_goal > away_team_goal AND NOT (BWH <= BWD AND BWH <= BWA) THEN 0 WHEN home_team_goal = away_team_goal AND (BWD < BWH AND BWD < BWA) THEN BWD WHEN home_team_goal = away_team_goal AND NOT (BWD < BWH AND BWD < BWA) THEN 0 WHEN home_team_goal < away_team_goal AND (BWA < BWH AND BWA < BWD) THEN BWA WHEN home_team_goal < away_team_goal AND NOT (BWA < BWH AND BWA < BWD) THEN 0 ELSE null END) AS payout_BW, AVG(CASE WHEN home_team_goal > away_team_goal AND (LBH <= LBD AND LBH <= LBA) THEN LBH WHEN home_team_goal > away_team_goal AND NOT (LBH <= LBD AND LBH <= LBA) THEN 0 WHEN home_team_goal = away_team_goal AND (LBD < LBH AND LBD < LBA) THEN LBD WHEN home_team_goal = away_team_goal AND NOT (LBD < LBH AND LBD < LBA) THEN 0 WHEN home_team_goal < away_team_goal AND (LBA < LBH AND LBA < LBD) THEN LBA WHEN home_team_goal < away_team_goal AND NOT (LBA < LBH AND LBA < LBD) THEN 0 ELSE null END) AS payout_LB, AVG(CASE WHEN home_team_goal > away_team_goal AND (WHH <= WHD AND WHH <= WHA) THEN WHH WHEN home_team_goal > away_team_goal AND NOT (WHH <= WHD AND WHH <= WHA) THEN 0 WHEN home_team_goal = away_team_goal AND (WHD < WHH AND WHD < WHA) THEN WHD WHEN home_team_goal = away_team_goal AND NOT (WHD < WHH AND WHD < WHA) THEN 0 WHEN home_team_goal < away_team_goal AND (WHA < WHH AND WHA < WHD) THEN WHA WHEN home_team_goal < away_team_goal AND NOT (WHA < WHH AND WHA < WHD) THEN 0 ELSE null END) AS payout_WH, AVG(CASE WHEN home_team_goal > away_team_goal AND (SJH <= SJD AND SJH <= SJA) THEN SJH WHEN home_team_goal > away_team_goal AND NOT (SJH <= SJD AND SJH <= SJA) THEN 0 WHEN home_team_goal = away_team_goal AND (SJD < SJH AND SJD < SJA) THEN SJD WHEN home_team_goal = away_team_goal AND NOT (SJD < SJH AND SJD < SJA) THEN 0 WHEN home_team_goal < away_team_goal AND (SJA < SJH AND SJA < SJD) THEN SJA WHEN home_team_goal < away_team_goal AND NOT (SJA < SJH AND SJA < SJD) THEN 0 ELSE null END) AS payout_SJ, AVG(CASE WHEN home_team_goal > away_team_goal AND (VCH <= VCD AND VCH <= VCA) THEN VCH WHEN home_team_goal > away_team_goal AND NOT (VCH <= VCD AND VCH <= VCA) THEN 0 WHEN home_team_goal = away_team_goal AND (VCD < VCH AND VCD < VCA) THEN VCD WHEN home_team_goal = away_team_goal AND NOT (VCD < VCH AND VCD < VCA) THEN 0 WHEN home_team_goal < away_team_goal AND (VCA < VCH AND VCA < VCD) THEN VCA WHEN home_team_goal < away_team_goal AND NOT (VCA < VCH AND VCA < VCD) THEN 0 ELSE null END) AS payout_VC, AVG(CASE WHEN home_team_goal > away_team_goal AND (GBH <= GBD AND GBH <= GBA) THEN GBH WHEN home_team_goal > away_team_goal AND NOT (GBH <= GBD AND GBH <= GBA) THEN 0 WHEN home_team_goal = away_team_goal AND (GBD < GBH AND GBD < GBA) THEN GBD WHEN home_team_goal = away_team_goal AND NOT (GBD < GBH AND GBD < GBA) THEN 0 WHEN home_team_goal < away_team_goal AND (GBA < GBH AND GBA < GBD) THEN GBA WHEN home_team_goal < away_team_goal AND NOT (GBA < GBH AND GBA < GBD) THEN 0 ELSE null END) AS payout_GB, AVG(CASE WHEN home_team_goal > away_team_goal AND (BSH <= BSD AND BSH <= BSA) THEN BSH WHEN home_team_goal > away_team_goal AND NOT (BSH <= BSD AND BSH <= BSA) THEN 0 WHEN home_team_goal = away_team_goal AND (BSD < BSH AND BSD < BSA) THEN BSD WHEN home_team_goal = away_team_goal AND NOT (BSD < BSH AND BSD < BSA) THEN 0 WHEN home_team_goal < away_team_goal AND (BSA < BSH AND BSA < BSD) THEN BSA WHEN home_team_goal < away_team_goal AND NOT (BSA < BSH AND BSA < BSD) THEN 0 ELSE null END) AS payout_BS FROM Match LEFT JOIN League l ON Match.league_id = l.id GROUP BY 1", conn)
conn.close()
df_favourite_PS_IW_leagues['rough_ave'] = (df_favourite_PS_IW_leagues['payout_PS'] + df_favourite_PS_IW_leagues['payout_IW'] + df_favourite_PS_IW_leagues['payout_B365'] + df_favourite_PS_IW_leagues['payout_BW'] + df_favourite_PS_IW_leagues['payout_LB'] + df_favourite_PS_IW_leagues['payout_WH'] + df_favourite_PS_IW_leagues['payout_SJ'] + df_favourite_PS_IW_leagues['payout_VC'] + df_favourite_PS_IW_leagues['payout_GB'] + df_favourite_PS_IW_leagues['payout_BS'])/10
df_favourite_PS_IW_leagues_sorted = df_favourite_PS_IW_leagues.sort_values('rough_ave', axis=0, ascending=False)
df_favourite_PS_IW_leagues_sorted

# Plot payout per league for PS and IW
df_favourite_PS_IW_leagues_sorted.plot(x="League", y=["payout_PS", "payout_IW", "payout_B365", "payout_BW", "payout_LB", "payout_WH", "payout_SJ", "payout_VC", "payout_GB", "payout_BS"], kind="bar", figsize=(10, 5))

# Add titles
plt.title("Payout rate of match favourite, by bookmaker and league", loc='left', fontsize=12, fontweight=0, color='black')
plt.ylabel("Payout rate");

# The actual likelihood of a home win, draw and loss, by league.

conn = sqlite3.connect('database.sqlite')
df_actual_results_leagues = pd.read_sql("SELECT l.name, AVG(CASE WHEN m.home_team_goal > m.away_team_goal THEN 1 ELSE 0 END) AS home_win, AVG(CASE WHEN m.home_team_goal = m.away_team_goal THEN 1 ELSE 0 END) AS home_draw, AVG(CASE WHEN m.home_team_goal < m.away_team_goal THEN 1 ELSE 0 END) AS home_loss FROM Match m LEFT JOIN League l ON m.league_id = l.id GROUP BY 1", conn)
conn.close()
df_actual_results_leagues.sort_values('home_win', axis=0, ascending=False)
