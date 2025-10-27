#!/usr/bin/env python3
import os
import aws_cdk as cdk
from python_app.python_app_stack import PythonAppStack

app = cdk.App()
PythonAppStack(app, "PythonAppStack",
    env=cdk.Environment(
        account=os.getenv('CDK_DEFAULT_ACCOUNT'),
        region=os.getenv('CDK_DEFAULT_REGION')
    )
)

app.synth()

