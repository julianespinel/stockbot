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
               "Effect": "Allow",
               "Action": [
                   "sts:AssumeRole"
               ],
               "Resource": [
                   "arn:aws:iam::*:role/cdk-*"
               ]
           }
       ]
   }
   ```

## Deploy

1. Run the following command to create the infrastructure and deploy the code:
    ```bash
    make deploy
    ```

2. Set Telegram bot webhook:
    ```bash
    GET https://api.telegram.org/bot{my_bot_token}/setWebhook?url={url_to_send_updates_to}
    ```

3. Verify webhook was set:
    ```bash
    GET https://api.telegram.org/bot{my_bot_token}/getWebhookInfo
    ```

4. Send a message to the Bot using the Telegram client (web, mobile, etc).


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
