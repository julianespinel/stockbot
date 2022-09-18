from aws_cdk import (aws_apigateway as apigateway, aws_lambda, Duration)
from constructs import Construct

import env_validator


class PushService(Construct):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

        telegram_token = env_validator.get_or_throw('TELEGRAM_BOT_TOKEN')
        channel_id = env_validator.get_or_throw('CHANNEL_ID')

        handler = aws_lambda.DockerImageFunction(
            scope=self,
            id='Stockbot',
            function_name='Stockbot',
            code=aws_lambda.DockerImageCode.from_image_asset(
                directory='../src',
                cmd=['push.lambda_handler'],
            ),
            timeout=Duration.seconds(30),  # Default is only 3 seconds
            environment={
                'TELEGRAM_BOT_TOKEN': telegram_token,
                'CHANNEL_ID': channel_id,
            },
        )

        api = apigateway.RestApi(
            self, 'stockbot-api',
            rest_api_name='Stockbot Service',
            description='API gateway for stockbot'
        )

        get_stockbot_integration = apigateway.LambdaIntegration(
            handler,
            request_templates={"application/json": '{ "statusCode": "200" }'}
        )

        api.root.add_method('POST', get_stockbot_integration)
