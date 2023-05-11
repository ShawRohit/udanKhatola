import os


class QaDevelepment:
    db_name = 'qadubbingnuvek'
    db_username = 'qadubbing'
    db_password = 'WEJhyuX209#WqH'
    db_host = 'localhost'
    base_url = "http://192.168.0.34:5000/"
    region_name = os.environ['REGION_NAME']
    aws_access_key_id = os.environ['aws_access_key_id']
    aws_secret_access_key = os.environ['aws_secret_access_key']
    USER_POOL_ID = os.environ['USER_POOL_ID']
    CLIENT_ID = os.environ['CLIENT_ID']
    CLIENT_SECRET = os.environ['CLIENT_SECRET']
    upload_folder = 'uploads'
    S3_REGION_NAME = "us-east-1"
    S3_IMAGE_FOLDER = os.environ['S3_IMAGE_FOLDER']
    S3_EPISODE_IMAGE_FOLDER = os.environ['S3_EPISODE_IMAGE_FOLDER']
    S3_BUCKET_NAME = os.environ['S3_BUCKET_NAME']
