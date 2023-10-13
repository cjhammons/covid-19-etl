#------------------------------------
# Author: Curtis Hammons (cjhammons)
# Email: curtishammons@gmail.com
# Created: 2023-10-12
#------------------------------------
import pandas as pd

# Calculate incremental daily cases and deaths per day per state
def calculate_incremental(df):
    df_incremental = df.sort_values(by=['state_name', 'date'])
    df_incremental['daily_cases'] = df_incremental.groupby('state_name')['cases'].diff().fillna(0)
    df_incremental['daily_deaths'] = df_incremental.groupby('state_name')['deaths'].diff().fillna(0)
    return df_incremental[['date', 'state_name', 'Cases', 'Deaths']].rename(columns={'date': 'Date', 'state_name': 'State'})

# Calculate a rolling average, per state, of cases and deaths in the last seven days
def calculate_rolling_avg(df):
    df['Rolling Avg Cases'] = df.groupby('state_name')['daily_cases'].transform(lambda x: x.rolling(window=7).mean())
    df['Rolling Avg Deaths'] = df.groupby('state_name')['daily_deaths'].transform(lambda x: x.rolling(window=7).mean())
    return df[['Date', 'State', 'Rolling Avg Cases', 'Rolling Avg Deaths']]


def calculate_mask_wearer_score(df_mask_use, df_county_population):
    df_mask_score = pd.merge(df_mask_use, df_county_population, on='fips')
    df_mask_score['Share Would Wear'] = df_mask_score['always'] + df_mask_score['frequently']
    df_mask_score['Share Would Not Wear'] = df_mask_score['never'] + df_mask_score['rarely']
    df_mask_score['Net Mask Wearer Score'] = (df_mask_score['Share Would Wear'] - df_mask_score['Share Would Not Wear']) * df_mask_score['population_estimate_2020']
    df_mask_score = df_mask_score.nlargest(10, 'Net Mask Wearer Score')
    df_mask_score['Rank'] = range(1, len(df_mask_score) + 1)
    return df_mask_score[['Rank', 'fips', 'county_name', 'state_name', 
                          'Share Would Wear', 'Share Would Not Wear', 
                          'population_estimate_2020', 'Net Mask Wearer Score']
                           ].rename(columns={'fips': 'FIPS', 'county_name': 'County', 'state_name': 'State', 'population_estimate_2020': 'Population'})


