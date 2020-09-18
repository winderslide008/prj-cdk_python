#!/usr/bin/env python3

from aws_cdk import core

from prj_cdk_python.prj_cdk_python_stack import PrjCdkPythonStack


app = core.App()
PrjCdkPythonStack(app, "prj-cdk-python")

app.synth()
