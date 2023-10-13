# Covid-19 ETL

This ETL is a dockerized application that uses batch processing to:
- Extract data from a postgresql database running in AWS RDS
- Transforms the data using Pandas by performing calculations and adding them to the dataframe
- Loads the data into CSV files which are then stored in S3

The exported CSV files can also be found in the ``export/`` directory.

# The Code

In the ``src`` directory there are 4 python files that contain the application logic:
- ``Extract.py`` contains the logic to extract the data from RDS
- ``Transform.py`` performs the calculation logic 
- ``Load.py`` exports the data into .csv files which are uploaded to an S3 bucket
- ``main.py`` which loads config variables and calls the functions in order.

# Deployment

The app is running as a CronJob in EKS set to execute on the hour. I used a bash script ``build/build-and-deploy.sh`` to build the docker image, deploy it to ECR, then deploy it from ECR to EKS.

# Run Locally

To run locally you first need to install the dependencies:

```bash
pip install -r requirements.txt
```

A ``config.ini`` is required to connect to cloud services. Here is how my local one is formatted:
```ini
[DB]
user=<user>
password=<password>
host=<hostname>
port=<port>
database=<db-name>


[AWS]
access_key=<your access key>
secret_access_key=<your secret access key>
region_name=<your region>

[S3]
bucket_name=<s3 bucketname>

```

Then the application can be run with:
```bash
python src/main.py
```