from aws_cdk import (
    core
)

from prj_cdk_python.prj_cdk_python_stack import PrjCdkPythonStack


class PipelineStage(core.Stage):

    def __init__(self, scope: core.Construct, id: str, *, env: core.Environment) -> None:
        super().__init__(scope, id, env=env)

        my_stack = PrjCdkPythonStack(self, "Ec2Nginx")
