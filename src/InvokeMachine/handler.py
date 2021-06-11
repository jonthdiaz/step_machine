import os
import json
import time
import logging

from http import HTTPStatus

import boto3

BUCKET_DEST_NAME = "core-demo-dest"
boto_session = boto3.Session()


aws_client = boto_session.client(
    "stepfunctions", endpoint_url=os.environ.get("AWS_ENDPOINT_URL", None)
)

client_s3 = boto_session.client(
    "s3", endpoint_url=os.environ.get("AWS_ENDPOINT_URL", None)
)
PROCESS_FILE_MACHINE_ARN = os.environ.get("MACHINE_ARN")


def main(event, context):
    result = []
    for s3_file in event.get("Records", []):
        logging.info(s3_file)
        response = aws_client.start_execution(
            stateMachineArn=PROCESS_FILE_MACHINE_ARN,
            input=json.dumps(s3_file),
        )
        logging.info("Result state machine")
        logging.info(response)
    return response


def get_file_type_image(event, context):
    filename = event["s3"]["object"]["key"]
    return filename[filename.rfind(".") + 1 :]


def copy_image(event, context):
    bucket = event["s3"]["bucket"]["name"]
    file_name = event["s3"]["object"]["key"]

    # Copy file
    s3_file = client_s3.get_object(Bucket=bucket, Key=file_name)
    contents = s3_file["Body"].read()

    # Upload the file to the new bucket
    file_name_dest = (
        f"{file_name[:file_name.rfind('.')]}-machine-copy-{int(time.time())}.jpeg"
    )
    client_s3.put_object(
        Bucket=BUCKET_DEST_NAME,
        Key=file_name_dest,
        Body=contents,
        ACL="public-read",
        ContentType="image/jpeg",
    )
    return "Done Machine Copy!"


def resize_image(event, context):
    bucket = event["s3"]["bucket"]["name"]
    file_name = event["s3"]["object"]["key"]

    # Copy file
    s3_file = client_s3.get_object(Bucket=bucket, Key=file_name)
    contents = s3_file["Body"].read()

    # Upload the file to the new bucket
    file_name_dest = (
        f"{file_name[:file_name.rfind('.')]}-machine-resize-{int(time.time())}.jpeg"
    )
    client_s3.put_object(
        Bucket=BUCKET_DEST_NAME,
        Key=file_name_dest,
        Body=contents,
        ACL="public-read",
        ContentType="image/jpeg",
    )
    return "Done Machine Resize!"


def delete_image(event, context):
    bucket = event["s3"]["bucket"]["name"]
    file_name = event["s3"]["object"]["key"]

    client_s3.delete_object(Bucket=bucket, Key=file_name)

    return True
