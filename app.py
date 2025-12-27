#!/usr/bin/env python3
import aws_cdk as cdk
from mlflow_stack import SimpleMLflowStack

app = cdk.App()

SimpleMLflowStack(
    app,
    "MLflowStack",
    env=cdk.Environment(
        account="<your-aws-account-id>", # <-- CHANGE THIS
        region="<your-aws-sagemaker-domain-region>", # <-- CHANGE THIS
    ),
)

app.synth()
