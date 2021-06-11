# -*- coding: utf-8 -*-
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


def main(event, context):
    result = []
    response = aws_client.start_execution(
        stateMachineArn="arn:aws:states:us-west-1:672646104180:stateMachine:MyStateMachine",
        input=json.dumps({"results": {"fileType": "jpg"}}),
    )
    logging.error(response)

    return {
        "statusCode": HTTPStatus.OK,
        "body": json.dumps({"result": "executed"}),
    }
