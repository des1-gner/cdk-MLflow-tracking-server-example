from aws_cdk import (
    Stack,
    CfnOutput,
    RemovalPolicy,
    aws_s3 as s3,
    aws_iam as iam,
    aws_sagemaker as sagemaker,
)
from constructs import Construct


class SimpleMLflowStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # 1. S3 Bucket for artifacts
        bucket = s3.Bucket(
            self,
            "MLflowBucket",
            bucket_name=f"mlflow-artifacts-{self.account}",
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )

        # 2. IAM Role for tracking server
        role = iam.Role(
            self,
            "MLflowRole",
            assumed_by=iam.ServicePrincipal("sagemaker.amazonaws.com"),
        )
        bucket.grant_read_write(role)

        # 3. Create tracking server
        server = sagemaker.CfnMlflowTrackingServer(
            self,
            "TrackingServer",
            artifact_store_uri=f"s3://{bucket.bucket_name}/mlflow",
            role_arn=role.role_arn,
            tracking_server_name="your-mlflow-server-name",
            tracking_server_size="Small",
        )

        # Outputs
        CfnOutput(self, "BucketName", value=bucket.bucket_name)
        CfnOutput(self, "ServerName", value=server.tracking_server_name)
        CfnOutput(self, "ServerArn", value=server.attr_tracking_server_arn)
