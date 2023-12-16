import configparser
from pathlib import Path


parser= configparser.ConfigParser()
parser.read(Path(__file__).parent.resolve().joinpath('config.ini'))

AWS_ACCESS_KEY_ID = parser.get('aws', 'aws_access_key_id')
AWS_SECRET_ACCESS_KEY = parser.get('aws', 'aws_secret_access_key')
AWS_REGION = parser.get('aws', 'aws_region')
BUCKET_NAME = parser.get('aws', 'aws_bucket_name')
