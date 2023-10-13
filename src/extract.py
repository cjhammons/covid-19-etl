#------------------------------------
# Author: Curtis Hammons (cjhammons)
# Email: curtishammons@gmail.com
# Created: 2023-10-12
#------------------------------------
import pandas as pd

# Extract county_population table into a DataFrame
def extract_county_population(engine=None, logger=None):
    query = "SELECT * FROM county_population;"
    if logger:
        logger.info("Extracting county_population")
        logger.info("Query: %s" % query)
    try:
        df_county_population = pd.read_sql(query, engine)
    except Exception as e:
        if logger:
            logger.error("Could not extract county_population: %s" % e)
        exit(1)
    if logger:
        logger.info("Extraction complete")
        logger.info("DataFrame shape: %s" % str(df_county_population.shape))
    return df_county_population

# Extract mask_use_by_county table into a DataFrame
def extract_mask_use_by_county(engine=None, logger=None):
    query = "SELECT * FROM mask_use_by_county;"
    if logger:
        logger.info("Extracting mask_use_by_county")
        logger.info("Query: %s" % query)
    try:
        df_mask_use_by_county = pd.read_sql(query, engine)
    except Exception as e:
        if logger:
            logger.error("Could not extract mask_use_by_county: %s" % e)
        exit(1)
    if logger:
        logger.info("Extraction complete")
        logger.info("DataFrame shape: %s" % str(df_mask_use_by_county.shape))
    return df_mask_use_by_county

# Extract us_state_cumulative table into a DataFrame
def extract_us_state_cumulative(engine=None, logger=None):
    query = "SELECT * FROM us_state_cumulative;"
    if logger:
        logger.info("Extracting us_state_cumulative")
        logger.info("Query: %s" % query)
    try:
        df_us_state_cumulative = pd.read_sql(query, engine)
    except Exception as e:
        if logger:
            logger.error("Could not extract us_state_cumulative: %s" % e)
        exit(1)
    return df_us_state_cumulative


