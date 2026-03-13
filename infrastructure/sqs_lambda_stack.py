"""
CDK Stack for SQS, S3, and Lambda Functions
"""
from aws_cdk import (
    Stack,
    aws_sqs as sqs,
    aws_s3 as s3,
    aws_lambda as lambda_,
    aws_lambda_event_sources as event_sources,
    aws_iam as iam,
    Duration,
    RemovalPolicy,
)
from constructs import Construct
import os


class SqsLambdaStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create S3 bucket for Excel sheets
        self.excel_bucket = s3.Bucket(
            self,
            "ExcelSheetsBucket",
            bucket_name=f"excel-sheets-{self.account}-{self.region}",
            removal_policy=RemovalPolicy.DESTROY,  # Change to RETAIN for production
            auto_delete_objects=True,  # Change to False for production
            versioned=False,
        )

        # Create SQS Queue
        self.sqs_queue = sqs.Queue(
            self,
            "ExcelProcessingQueue",
            queue_name="excel-processing-queue",
            visibility_timeout=Duration.minutes(6),  # Should be > Lambda timeout
            retention_period=Duration.days(14),
            receive_message_wait_time=Duration.seconds(20),  # Long polling
        )

        # Create Dead Letter Queue
        dlq = sqs.Queue(
            self,
            "ExcelProcessingDLQ",
            queue_name="excel-processing-dlq",
            retention_period=Duration.days(14),
        )

        # Configure DLQ for main queue
        self.sqs_queue.add_to_queue_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                principals=[iam.ServicePrincipal("sqs.amazonaws.com")],
                actions=["sqs:SendMessage"],
                resources=[dlq.queue_arn],
            )
        )

        # Lambda execution role
        lambda_role = iam.Role(
            self,
            "LambdaExecutionRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "service-role/AWSLambdaBasicExecutionRole"
                )
            ],
        )

        # Grant permissions to Lambda to write to S3
        self.excel_bucket.grant_write(lambda_role)

        # Grant permissions to Lambda to read from SQS
        self.sqs_queue.grant_consume_messages(lambda_role)

        # Get the directory where this file is located
        infrastructure_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(infrastructure_dir)
        lambdas_dir = os.path.join(project_root, "lambdas")

        # Lambda Function 1: Data Processor
        data_processor_lambda = lambda_.Function(
            self,
            "DataProcessorLambda",
            function_name="excel-data-processor",
            runtime=lambda_.Runtime.PYTHON_3_11,
            handler="data_processor.handler",
            code=lambda_.Code.from_asset(
                os.path.join(lambdas_dir, "data_processor")
            ),
            role=lambda_role,
            timeout=Duration.minutes(5),
            memory_size=512,
            environment={
                "S3_BUCKET_NAME": self.excel_bucket.bucket_name,
            },
        )

        # Lambda Function 2: Excel Generator
        excel_generator_lambda = lambda_.Function(
            self,
            "ExcelGeneratorLambda",
            function_name="excel-generator",
            runtime=lambda_.Runtime.PYTHON_3_11,
            handler="excel_generator.handler",
            code=lambda_.Code.from_asset(
                os.path.join(lambdas_dir, "excel_generator")
            ),
            role=lambda_role,
            timeout=Duration.minutes(5),
            memory_size=512,
            environment={
                "S3_BUCKET_NAME": self.excel_bucket.bucket_name,
            },
        )

        # Connect SQS to Lambda Functions
        # Both lambdas will process messages from the same queue
        data_processor_lambda.add_event_source(
            event_sources.SqsEventSource(
                self.sqs_queue,
                batch_size=1,  # Process one message at a time
                max_batching_window=Duration.seconds(5),
            )
        )

        excel_generator_lambda.add_event_source(
            event_sources.SqsEventSource(
                self.sqs_queue,
                batch_size=1,  # Process one message at a time
                max_batching_window=Duration.seconds(5),
            )
        )

        # Outputs
        self.add_output("QueueUrl", self.sqs_queue.queue_url)
        self.add_output("QueueArn", self.sqs_queue.queue_arn)
        self.add_output("BucketName", self.excel_bucket.bucket_name)
        self.add_output("DataProcessorFunctionName", data_processor_lambda.function_name)
        self.add_output("ExcelGeneratorFunctionName", excel_generator_lambda.function_name)

    def add_output(self, key: str, value: str):
        """Helper method to add stack outputs"""
        from aws_cdk import CfnOutput
        CfnOutput(self, key, value=value)

