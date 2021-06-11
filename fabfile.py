# -*- coding: utf-8 -*-
import json
import os
import pathlib
import sys
import time
from enum import Enum

from fabric.api import abort, cd, env, local, parallel, put, run, sudo
from fabric.colors import red
from fabric.context_managers import prefix
from fabric.contrib.files import exists
from fabric.operations import prompt


class Region(Enum):
    VIRGINIA = "us-east-1"  # for dev
    CALIFORNIA = "us-west-1"  # for qe


env.aws_region = Region.CALIFORNIA.value
env.bucket_name = "sam-storage-machine-dev"
env.path = pathlib.Path(__file__).parent.absolute()


def create_sam_bucket():
    """
    this command only must run  once time"""
    local(f"aws s3 mb s3://{env.bucket_name} --region {env.aws_region}")


def deploy_stack():
    """
    This function makes the deploy of Hybrid service stack
    """
    build = "sam build --use-container --manifest src/images/requirements.txt"
    local(build)

    #package = f"sam package --template-file template.yaml --output-template-file \
    #            packaged.yaml --s3-bucket {env.bucket_name} --region {env.aws_region}"
    #local(package)

    deploy = f"sam deploy --stack-name storge-machine-service \
                --s3-bucket {env.bucket_name}\
                --parameter-overrides  env=dev --capabilities CAPABILITY_IAM CAPABILITY_AUTO_EXPAND --region {env.aws_region}"
    #deploy = "sam deploy"
    local(deploy)
