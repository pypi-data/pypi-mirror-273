from typing import Any

import boto3


class Uploader:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.client = boto3.client("s3", *args, **kwargs)

    def upload(self, bucket_name: str, destination_filename: str, source_filename: str) -> None:
        self.client.upload_file(source_filename, bucket_name, destination_filename)
