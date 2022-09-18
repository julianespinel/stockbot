from aws_cdk import Stack
from constructs import Construct

from push_service import PushService
from monitor_service import MonitorService


class StockbotStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines our stack goes here
        PushService(self, "PushService")
        MonitorService(self, "MonitorService")
