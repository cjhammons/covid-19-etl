#------------------------------------
# Author: Curtis Hammons (cjhammons)
# Email: curtishammons@gmail.com
# Created: 2023-10-12
#------------------------------------

import boto3
import pandas as pd

def load_to_csv(df, filename):
    file_path = 'data/' + filename
    df.to_csv(file_path, index=False)
    return file_path
    
def upload_to_s3(bucket_name, file_path, object_name=None, s3_client=None):
    s3 = s3_client
    if s3 is None:
        s3 = boto3.client('s3')
    if object_name is None:
        object_name = file_path
    try:
        s3.upload_file(file_path, bucket_name, object_name)
        print(f"Successfully uploaded {file_path} to {bucket_name}.")
    except Exception as e:
        print(f"Could not upload to S3: {e}")