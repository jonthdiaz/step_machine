# -*- coding: utf-8 -*-
import os
import json
import time
import logging

from http import HTTPStatus

import boto3

BUCKET_DEST_NAME = "core-demo-dest"
boto_session = boto3.Session()

client_s3 = boto_session.client(
    "s3", endpoint_url=os.environ.get("AWS_ENDPOINT_URL", None)
)


def main(event, context):
    result = []
    for s3_file in event.get("Records", []):
        bucket = s3_file["s3"]["bucket"]["name"]
        file_name = s3_file["s3"]["object"]["key"]

        # Copy file
        s3_file = client_s3.get_object(Bucket=bucket, Key=file_name)
        contents = s3_file["Body"].read()

        # Upload the file to the new bucket
        file_name_dest = (
            f"{file_name[:file_name.rfind('.')]}-dest-{int(time.time())}.jpg"
        )
        client_s3.put_object(
            Bucket=BUCKET_DEST_NAME,
            Key=file_name_dest,
            Body=contents,
            ACL="public-read",
            ContentType="image/jpeg"
        )
    return {
        "statusCode": HTTPStatus.OK,
        "body": json.dumps({"result": "file copied"}),
    }
