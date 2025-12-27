# MLflow Tracking Server with SageMaker Domain Integration

This repository provides a simple AWS CDK implementation for creating an MLflow Tracking Server that integrates with an existing SageMaker Domain.

## Overview

The MLflow Tracking Server and SageMaker Domain do not require explicit linking at the CloudFormation level. Integration occurs automatically through IAM permissions and regional co-location. This example demonstrates the minimal configuration needed to deploy a tracking server and configure the necessary permissions for Studio access.

## Prerequisites

- An existing SageMaker Domain
- AWS CLI configured with appropriate credentials
- Node.js and npm installed
- Python 3.7 or later

## Project Structure

```
cdk-MLflow-tracking-server-example/
├── app.py                    # CDK application entry point
├── mlflow_stack.py          # Stack definition with tracking server resources
├── mlflow-policy.json       # IAM policy for domain execution role
├── requirements.txt         # Python dependencies
└── cdk.json                 # CDK configuration
```

## Setup Instructions

### 1. Install Dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
npm install -g aws-cdk
```

### 2. Configure Account and Region

Edit `app.py` and update the following values:

- Replace `<your-aws-account-id>` with your AWS account ID
- Replace `<your-aws-sagemaker-domain-region>` with your desired AWS region

### 3. Customize Tracking Server Name (Optional)

Edit `mlflow_stack.py` and locate the `tracking_server_name` parameter. Change it to your desired name:

```python
tracking_server_name="your-mlflow-server-name",
```

### 4. Update S3 Bucket Reference

Edit `mlflow-policy.json` and update the S3 bucket ARN in both Resource entries:

- Replace `<your-aws-account-id>` with your AWS account ID in both lines containing the S3 bucket ARN

### 5. Deploy the Tracking Server

```bash
cdk bootstrap
cdk deploy
```

Deployment takes approximately 5-20 minutes. Upon completion, the stack outputs will include the tracking server name, ARN, and S3 bucket name.

### 6. Configure Domain Execution Role Permissions

Retrieve your SageMaker Domain execution role name:

```bash
aws sagemaker describe-domain --domain-id YOUR_DOMAIN_ID --query 'DefaultUserSettings.ExecutionRole' --output text
```

Attach the MLflow permissions to the execution role:

```bash
aws iam put-role-policy \
  --role-name YOUR_ROLE_NAME \
  --policy-name MLflowAccess \
  --policy-document file://mlflow-policy.json
```

Replace `YOUR_ROLE_NAME` with the role name from the previous command (not the full ARN, just the role name).

## Accessing the Tracking Server

After completing the setup:

1. Refresh your SageMaker Studio browser session
2. The MLflow Tracking Server will appear automatically in the Studio UI
3. Navigate to the MLflow section to access the tracking server interface

If the tracking server does not appear immediately, restart your Studio application or wait a few minutes for permissions to propagate.

## Verification

Confirm the tracking server status:

```bash
aws sagemaker list-mlflow-tracking-servers
aws sagemaker describe-mlflow-tracking-server --tracking-server-name your-mlflow-server-name
```

Replace `your-mlflow-server-name` with the tracking server name you configured in step 3.

## Cleanup

To remove all resources:

```bash
cdk destroy
```

Note: Remove the inline policy from your domain execution role manually if no longer needed:

```bash
aws iam delete-role-policy \
  --role-name YOUR_ROLE_NAME \
  --policy-name MLflowAccess
```

## Resources

- [AWS CDK Python Reference](https://docs.aws.amazon.com/cdk/api/v2/python/)
- [CfnMlflowTrackingServer Documentation](https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_sagemaker/CfnMlflowTrackingServer.html)
- [Create an MLflow Tracking Server](https://docs.aws.amazon.com/sagemaker/latest/dg/mlflow-create-tracking-server.html)
- [MLflow Tracking Server IAM Permissions](https://docs.aws.amazon.com/sagemaker/latest/dg/mlflow-tracking-server-iam.html)
