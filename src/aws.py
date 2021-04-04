from typing import Optional
from pathlib import Path

import boto3

from config_aws import S3Config

conf = S3Config()
conf.make_config()

# session = boto3.Session(aws_access_key_id=conf.user,aws_secret_access_key=conf.key)

class S3Manager:

    def __init__(self, bucket_name : Optional[str] = None):
        self.__s3 = boto3.resource('s3')
        self.__bucket_name = bucket_name if bucket_name is not None else conf.bucket_name
        self.bucket = None

    def __get_bucket(self) -> object:
        if self.bucket is None:
            for bucket in self.__s3.buckets.all():
                if bucket.name == self.__bucket_name:
                    self.bucket = bucket
                    return bucket
            return None
        else:
            return self.bucket

    def connect(self) -> bool:
        bucket = self.__get_bucket()
        if bucket is None:
            bucket = self.__s3.Bucket(self.__bucket_name)
            resp = bucket.create(
                ACL='private',
                CreateBucketConfiguration={
                    'LocationConstraint': conf.region
                },
            )
            if ("ResponseMetadata" not in resp) \
                    or (resp['ResponseMetadata']['HTTPStatusCode']!=200):
                return False
            else:
                self.bucket = bucket
        return bucket.name == self.__bucket_name

    def upload_file(self, path: str, file_name: str) -> bool:
        self.__s3.Object(self.__bucket_name,file_name).upload_file(str(Path(path)/file_name))
        return True