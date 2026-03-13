#!/usr/bin/env python3
"""
AWS CDK App for SQS Service with Lambda Functions
"""
import aws_cdk as cdk
from sqs_lambda_stack import SqsLambdaStack

app = cdk.App()
SqsLambdaStack(
    app,
    "SqsExcelServiceStack",
    env=cdk.Environment(
        account=app.node.try_get_context("account") or None,
        region=app.node.try_get_context("region") or "us-east-1",
    ),
    description="SQS service that triggers Lambda functions to generate Excel sheets in S3"
)

app.synth()

