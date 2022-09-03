from aws_cdk import Stack
from constructs import Construct

from stockbot_service import StockbotService


class StockbotStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        StockbotService(self, "StockbotService")
