#!/usr/bin/env python

import aws_cdk as cdk

from stack import StockbotStack

app = cdk.App()
StockbotStack(app, "StockbotStack")
app.synth()
