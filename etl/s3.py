import logging
import sys
import boto3
import botocore
from pathlib import Path


# Add the project directory to path, in order to import modules
sys.path.append(str(Path(__file__).parent.parent.resolve()))

from config.constant import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, BUCKET_NAME, AWS_REGION

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s:%(funcName)s:%(levelname)s:%(message)s')

def connect_to_s3():
    try:
        session = boto3.Session(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION
        )
        conn = session.client('s3')
        logging.info('Connection Successful')
        return conn
    except Exception as e:
        print(f"Can't connect to S3. Error: {e}")


def create_bucket_if_not_exist(conn):
    try:
        conn.head_bucket(Bucket=BUCKET_NAME)
        # conn.meta.client.head_bucket(Bucket=BUCKET_NAME)
        logging.info(f'The bucket {BUCKET_NAME} exists already.')
    except botocore.exceptions.ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == '404':
            logging.info('Bucket does not exit')
            conn.create_bucket(
                bucket=BUCKET_NAME,
                CreateBucketConfiguration={'LocationConstraint': AWS_REGION}
            )
    

def upload_to_s3(conn, file_path,bucket, s3_object_name):
    try:
        conn.upload_file(file_path,bucket, s3_object_name)
        logging.info('File successfully uploaded to S3!')
    except FileNotFoundError:
        logging.info('The file was not found!')


def s3_pipeline(ti): 

    file_path = ti.xcom_pull(task_ids='faker_extract', key='return_value')
    bucket = BUCKET_NAME
    conn = connect_to_s3()
    create_bucket_if_not_exist(conn)
    upload_to_s3(conn,file_path,bucket, s3_object_name=file_path.split('/')[-1])


if __name__ =='__main__':
    s3_pipeline()