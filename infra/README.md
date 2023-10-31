# Deploy using CDK

We use AWS CDK to manage the infrastructure using regular Python code.

## Prerequisites

We need to have the following software installed in our localhost:

1. Docker
2. CDK CLI
3. Create an IAM user with the following permission policy to be used by CDK:
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Sid": "sts",
         "Effect": "Allow",
         "Action": [
           "sts:AssumeRole"
         ],
         "Resource": [
           "*"
         ]
       },
       {
         "Action": [
           "cloudformation:CreateChangeSet",
           "cloudformation:DeleteStack",
           "cloudformation:DescribeChangeSet",
           "cloudformation:DescribeStackEvents",
           "cloudformation:DescribeStacks",
           "cloudformation:ExecuteChangeSet",
           "cloudformation:GetTemplate",
           "cloudformation:DeleteChangeSet"
         ],
         "Resource": [
           "arn:aws:cloudformation:*:*:stack/*/*"
         ],
         "Effect": "Allow",
         "Sid": "CloudFormationPermissions"
       },
       {
         "Action": [
           "iam:CreateRole",
           "iam:DeleteRole",
           "iam:GetRole",
           "iam:AttachRolePolicy",
           "iam:DetachRolePolicy",
           "iam:DeleteRolePolicy",
           "iam:PutRolePolicy",
           "iam:PassRole"
         ],
         "Effect": "Allow",
         "Resource": [
           "arn:aws:iam::*:policy/*",
           "arn:aws:iam::*:role/cdk-*"
         ]
       },
       {
         "Action": [
           "s3:CreateBucket",
           "s3:DeleteBucket",
           "s3:PutBucketPolicy",
           "s3:DeleteBucketPolicy",
           "s3:PutBucketPublicAccessBlock",
           "s3:PutBucketVersioning",
           "s3:PutEncryptionConfiguration",
           "s3:PutLifecycleConfiguration",
           "s3:GetBucketLocation",
           "s3:ListBucket",
           "s3:GetObject",
           "s3:DeleteObject",
           "s3:PutObject"
         ],
         "Effect": "Allow",
         "Resource": [
           "arn:aws:s3:::cdk-*"
         ]
       },
       {
         "Action": [
           "ssm:DeleteParameter",
           "ssm:GetParameter",
           "ssm:GetParameters",
           "ssm:PutParameter"
         ],
         "Effect": "Allow",
         "Resource": [
           "arn:aws:ssm:*:*:parameter/cdk-bootstrap/*"
         ]
       },
       {
         "Action": [
           "ecr:CreateRepository",
           "ecr:DeleteRepository",
           "ecr:DescribeRepositories",
           "ecr:SetRepositoryPolicy",
           "ecr:PutLifecyclePolicy",
           "ecr:DescribeImages"
         ],
         "Effect": "Allow",
         "Resource": [
           "arn:aws:ecr:*:*:repository/cdk-*"
         ]
       }
     ]
   }
   ```

## Deploy

1. Set the following environment variables:
    ```bash
    export AWS_ACCESS_KEY_ID='<access-key-id>'
    export AWS_SECRET_ACCESS_KEY='<secret-access-key>'
    export CDK_DEPLOY_REGION='<aws-region>'
    export CDK_DEPLOY_ACCOUNT='<aws-account-id>'
    ```

1. Run the following command to create the infrastructure and deploy the code:
    ```bash
    make deploy
    ```

1. Set Telegram bot webhook:
    ```bash
    GET https://api.telegram.org/bot{my_bot_token}/setWebhook?url={url_to_send_updates_to}
    ```

1. Verify webhook was set:
    ```bash
    GET https://api.telegram.org/bot{my_bot_token}/getWebhookInfo
    ```

1. Send a message to the Bot using the Telegram client (web, mobile, etc).


## Destroy

If we want to delete the infrastructure created, please run this command:
```bash
make destroy
```

## Resources

1. [Install CDK](https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html)
2. [CDK API Gateway + Lambda example](https://docs.aws.amazon.com/cdk/v2/guide/serverless_example.html)
3. [An introduction to Telegram bots](https://core.telegram.org/bots)
4. [Telegram bot using webhooks on AWS Lambda](https://github.com/jojo786/Sample-Python-Telegram-Bot-AWS-Serverless)
5. [How to set Telegram bot webhook?](https://stackoverflow.com/questions/42554548/how-to-set-telegram-bot-webhook)
