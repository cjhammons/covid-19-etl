#!/usr/bin/python3

#------------------------------------
# Author: Curtis Hammons (cjhammons)
# Email: curtishammons@gmail.com
# Created: 2023-10-12
#------------------------------------
from extract import *
from transform import *
from load import *
import configparser
import pandas as pd
import logging
from sqlalchemy import create_engine

def main():
    # Set up logging
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    console_handler = logging.StreamHandler()
    logger.addHandler(console_handler)
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)

    # Extract data from DB
    # First we read the DB config from the config.ini file
    logger.info("Reading config.ini")
    config = configparser.ConfigParser()
    config.read("config.ini")
    host=config["DB"]["host"]
    port=config["DB"]["port"]
    database=config["DB"]["database"]
    user=config["DB"]["user"]
    password=config["DB"]["password"]
    connection_string = f'postgresql://{user}:{password}@{host}:{int(port)}/{database}'
    try:
        logger.info("Connecting to DB using string %s" % connection_string)
        engine = create_engine(connection_string)
    except Exception as e:
        logger.error("Could not connect to DB: %s" % e)
        exit(1)
    logger.info("Begining Extraction")

    logger.info("Extracting county_population")
    df_county_population = extract_county_population(engine, logger)

    logger.info("Extracting mask_use_by_county")
    df_mask_use_by_county = extract_mask_use_by_county(engine, logger)

    logger.info("Extracting us_state_cumulative")
    df_us_state_cumulative = extract_us_state_cumulative(engine, logger)

    logger.info("Extraction complete")
    logger.info("Closing DB connection")
    engine.dispose()
    
    # Transform data
    # We pass the extracted data to the transform functions
    logger.info("Begining Transformation")
    logger.info("Calculating incremental Cases and Deaths")
    df_incremental_data = calculate_incremental(df_us_state_cumulative)

    logger.info("Calculating rolling average Cases and Deaths")
    df_rolling_data = calculate_rolling_avg(df_incremental_data)

    logger.info("Calculating mask wearer score")
    df_mask_score = calculate_mask_wearer_score(df_mask_use_by_county, df_county_population)
    
    # Load to CSV and S3
    logger.info("Begining Load into S3")
    s3_client = boto3.client(
        's3',
        aws_access_key_id=config["AWS"]["access_key"],
        aws_secret_access_key=config["AWS"]["secret_access_key"],
        region_name=config["AWS"]["region_name"]
    )
    bucket_name = config["S3"]["bucket_name"]
    logger.info("Exporting Incremental Cases and Deaths to CSV")
    incremental_path = load_to_csv(df_incremental_data, 'incremental_data')
    
    logger.info("Exporting Rolling Average Cases and Deaths to CSV")
    rolling_path = load_to_csv(df_rolling_data, 'rolling_data')
    
    logger.info("Exporting Mask Wearer Score to CSV")
    mask_score_path = load_to_csv(df_mask_score, 'mask_score')

    logger.info("Uploading %s to S3" % incremental_path)
    upload_to_s3(bucket_name, incremental_path, s3_client=s3_client, logger=logger)

    logger.info("Uploading %s to S3" % rolling_path)
    upload_to_s3(bucket_name, rolling_path, s3_client=s3_client, logger=logger)

    logger.info("Uploading %s to S3" % mask_score_path)
    upload_to_s3(bucket_name, mask_score_path, s3_client=s3_client, logger=logger)

if __name__ == "__main__":
    main()