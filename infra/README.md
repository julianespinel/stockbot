# Deploy using CDK

We use AWS CDK to manage the infrastructure using regular Python code.

## Prerequisites

You need to have the following software installed in your localhost:

1. Docker
2. CDK CLI

## Deploy

Please run the following command to deploy the code:
```bash
make deploy
```

If you want to delete the infrastructure created, please run this command:
```bash
make destroy
```

## Resources

1. [Install CDK](https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html)
2. [CDK API Gateway + Lambda example](https://docs.aws.amazon.com/cdk/v2/guide/serverless_example.html)
3. [Telegram bot using wedbhooks on AWS Lambda](https://github.com/jojo786/Sample-Python-Telegram-Bot-AWS-Serverless)
