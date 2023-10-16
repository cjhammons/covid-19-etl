#------------------------------------
# Author: Curtis Hammons (cjhammons)
# Email: curtishammons@gmail.com
# Created: 2023-10-12
#------------------------------------

import boto3
import pandas as pd
import os 
import datetime

def load_to_csv(df, filename):
    # get current time and append to filename
    if not os.path.exists('export'):
        os.makedirs('export')
    now = datetime.datetime.now()
    file_path = filename + '_' + now.strftime("%Y-%m-%d_%H-%M-%S") + '.csv'

    df.to_csv('export/' + file_path, index=False)
    return file_path
    
def upload_to_s3(bucket_name, file_path, object_name=None, s3_client=None, logger=None):
    s3 = s3_client
    if s3 is None:
        if logger:
            logger.error("Could not connect to S3")
        exit(1)
    if object_name is None:
        object_name = file_path
    try:
        s3.upload_file(file_path, bucket_name, object_name)
        if logger:
            logger.info(f"Successfully uploaded {file_path} to {bucket_name}.")
    except Exception as e:
        if logger:
            logger.error(f"Could not upload {file_path} to {bucket_name}: {e}")