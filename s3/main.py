
import boto3, os

# AWS IAM User의 Access Key ID와 Secret Access Key
ACCESS_KEY = os.getenv('acc_key')
SECRET_KEY = os.getenv('sec_key')

# S3 Bucket 이름과 다운로드할 객체 이름
BUCKET_NAME = 'ocpp16'
OBJECT_NAME = 'Authorize.json'

# AWS IAM User의 자격 증명(Credentials) 생성
session = boto3.Session(
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY
)

# S3 객체를 다운로드하기 위한 S3 Client 생성
s3_client = session.client('s3')

# S3 객체 다운로드
s3_client.download_file(BUCKET_NAME, OBJECT_NAME, 'Authorize.json.downloaded')
with open(f'{OBJECT_NAME}.downloaded', "r", encoding="utf-8") as fd:
    print(fd.read())