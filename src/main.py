#------------------------------------
# Author: Curtis Hammons (cjhammons)
# Email: curtishammons@gmail.com
# Created: 2023-10-12
#------------------------------------
from extract import extract_data
from transform import *
from load import *

def main():
    data = extract_data()
    incremental_data = calculate_incremental(data)
    rolling_data = calculate_rolling_average(data)
    mask_score = calculate_mask_wearer_score(data)
    
    # Load to CSV and S3
    load_to_csv(incremental_data, "incremental.csv")
    upload_to_s3("incremental.csv", "s3_path")
    