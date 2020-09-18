#!/usr/bin/env python3

from aws_cdk import core

from prj_cdk_python.prj_cdk_python_pipeline_stack import PipelineStack

from aws_cdk import core

app = core.App()
env = core.Environment(region="eu-central-1", account="927534600513")
PipelineStack(app, "prj-cdk-python", env=env)

app.synth()
