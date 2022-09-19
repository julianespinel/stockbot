from aws_cdk import (
    aws_lambda,
    Duration,
    aws_events,
    aws_events_targets as targets
)
from constructs import Construct

import env_validator


class MonitorService(Construct):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

        telegram_token = env_validator.get_or_throw('TELEGRAM_BOT_TOKEN')
        channel_id = env_validator.get_or_throw('CHANNEL_ID')
        symbols = env_validator.get_or_throw('SYMBOLS')

        handler = aws_lambda.DockerImageFunction(
            scope=self,
            id='StockbotMonitor',
            function_name='StockbotMonitor',
            code=aws_lambda.DockerImageCode.from_image_asset(
                directory='../src',
                cmd=['monitor.lambda_handler'],
            ),
            timeout=Duration.minutes(10),
            environment={
                'TELEGRAM_BOT_TOKEN': telegram_token,
                'CHANNEL_ID': channel_id,
                'SYMBOLS': symbols,
            },
        )

        # Execute rule from Monday to Friday at 2200 UTC (1800 GMT-4)
        six_pm_utc = '22'
        event_rule = aws_events.Rule(
            scope=self,
            id='StockbotMonitorRule',
            schedule=aws_events.Schedule.cron(
                minute='0',
                hour=six_pm_utc,
                week_day='MON-FRI'
            ),
        )

        event_rule.add_target(targets.LambdaFunction(handler))
