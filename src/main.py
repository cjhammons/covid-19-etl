#------------------------------------
# Author: Curtis Hammons (cjhammons)
# Email: curtishammons@gmail.com
# Created: 2023-10-12
#------------------------------------
from extract import *
from transform import *
from load import *
import configparser
import psycopg2
import pandas as pd

def main():

    # Extract data from DB
    # First we read the DB config from the config.ini file
    configparser = configparser.ConfigParser()
    configparser.read("config.ini")
    conn = psycopg2.connect(
        host=configparser["DB"]["host"],
        port=configparser,
        database=configparser["DB"]["database"],
        user=configparser["DB"]["user"],
        password=configparser["DB"]["password"]
    )
    df_county_population = extract_county_population(conn)
    df_mask_use_by_county = extract_mask_use_by_county(conn)
    df_us_state_cumulative = extract_us_state_cumulative(conn)
    conn.close()
    
    # Transform data
    # We pass the extracted data to the transform functions
    df_incremental_data = calculate_incremental(df_us_state_cumulative)
    df_rolling_data = calculate_rolling_avg(df_incremental_data)
    df_mask_score = calculate_mask_wearer_score(df_mask_use_by_county, df_county_population)
    
    # Load to CSV and S3

    s3_client = boto3.client(
        's3',
        aws_access_key_id=configparser["AWS"]["aws_access_key_id"],
        aws_secret_access_key=configparser["AWS"]["aws_secret_access_key"],
        region_name=configparser["AWS"]["region_name"]
    )
    bucket_name = configparser["S3"]["bucket_name"]

    incremental_path = load_to_csv(df_incremental_data, 'incremental_data.csv')
    rolling_path = load_to_csv(df_rolling_data, 'rolling_data.csv')
    mask_score_path = load_to_csv(df_mask_score, 'mask_score.csv')

    upload_to_s3(bucket_name, incremental_path, s3_client=s3_client)
    upload_to_s3(bucket_name, rolling_path, s3_client=s3_client)
    upload_to_s3(bucket_name, mask_score_path, s3_client=s3_client)