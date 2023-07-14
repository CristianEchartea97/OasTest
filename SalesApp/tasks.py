import os
import boto3
# from botocore.client import Config


def get_s3_client():
    """Creates an AWS S3 client"""
    session = boto3.session.Session(
        region_name=os.environ.get("AWS_REGION"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        # config=Config(signature_version="s3v4"),
    )
    return session.client("s3")


def request_presigned_upload_url(key):
    """
    Generates a presigned URL for uploading a file to S3
    param key: The key to use for the object in S3
    """
    client = get_s3_client()
    return client.generate_presigned_url(
        "put_object",
        Params={
            "Bucket": os.environ.get("AWS_S3_BUCKET_INPUT"),
            "Key": key,
            # "key": 'test/test.csv'
        },
        ExpiresIn=3600,
    )
