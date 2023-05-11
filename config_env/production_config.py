import os

class Production:
    db_name = 'proddubbing'
    db_username = 'Dubbingprod'
    db_password = 'uzYGXWy0MfIOPALHWtIQ'
    db_host = 'proddubbing.c1gzylxakbue.us-east-1.rds.amazonaws.com'
    base_url = "http://3.235.200.91:5000/"
    region_name = os.environ['REGION_NAME']
    aws_access_key_id = os.environ['aws_access_key_id']
    aws_secret_access_key = os.environ['aws_secret_access_key']
    USER_POOL_ID = os.environ['USER_POOL_ID']
    CLIENT_ID = os.environ['CLIENT_ID']
    CLIENT_SECRET = os.environ['CLIENT_SECRET']
    upload_folder = 'uploads'
    S3_REGION_NAME = os.environ['REGION_NAME']
    S3_IMAGE_FOLDER = os.environ['S3_IMAGE_FOLDER']
    S3_EPISODE_IMAGE_FOLDER = os.environ['S3_EPISODE_IMAGE_FOLDER']
    S3_BUCKET_NAME = os.environ['S3_BUCKET_NAME']
