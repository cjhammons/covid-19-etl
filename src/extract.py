#------------------------------------
# Author: Curtis Hammons (cjhammons)
# Email: curtishammons@gmail.com
# Created: 2023-10-12
#------------------------------------

import psycopg2
import pandas as pd



# Extract county_population table into a DataFrame
def extract_county_population(conn=None):
    query = "SELECT * FROM county_population;"
    df_county_population = pd.read_sql(query, conn)
    conn.close()
    return df_county_population

# Extract mask_use_by_county table into a DataFrame
def extract_mask_use_by_county(conn=None):
    query = "SELECT * FROM mask_use_by_county;"
    df_mask_use_by_county = pd.read_sql(query, conn)
    conn.close()
    return df_mask_use_by_county

# Extract us_state_cumulative table into a DataFrame
def extract_us_state_cumulative(conn=None):
    query = "SELECT * FROM us_state_cumulative;"
    df_us_state_cumulative = pd.read_sql(query, conn)
    conn.close()
    return df_us_state_cumulative


