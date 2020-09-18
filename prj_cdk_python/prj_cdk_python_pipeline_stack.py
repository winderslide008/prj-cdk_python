from aws_cdk import (
    aws_codepipeline,
    aws_codepipeline_actions,
    pipelines,
    core,
)

from prj_cdk_python.prj_cdk_python_pipeline_stage import PipelineStage


class PipelineStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, *, env=None):
        super().__init__(scope, id, env=env)

        source_artifact = aws_codepipeline.Artifact()
        cloud_assembly_artifact = aws_codepipeline.Artifact()

        source_action = aws_codepipeline_actions.GitHubSourceAction(
            action_name="GitHub",
            output=source_artifact,
            oauth_token=core.SecretValue.secrets_manager("github-token"),
            # Replace these with your actual GitHub project name
            owner="winderslide008",
            repo="prj-cdk_python"
        )

        synth_action = pipelines.SimpleSynthAction.standard_npm_synth(
            source_artifact=source_artifact,
            cloud_assembly_artifact=cloud_assembly_artifact,
            install_command="npm install -g aws-cdk && npm update && python -m pip install -r requirements.txt",

            # Use this if you need a build step (if you're not using ts-node
            # or if you have TypeScript Lambdas that need to be compiled).
            build_command="npx cdk synth -o dist"
        )

        cdk_props = pipelines.CdkPipelineProps(synth_action=synth_action,
                                               source_action=source_action,
                                               cloud_assembly_artifact=cloud_assembly_artifact,
                                               pipeline_name="cdkPythonPipeline")

        # pipeline = pipelines.CdkPipeline(self, "pipe", cdk_props=cdk_props)

        pipeline = pipelines.CdkPipeline(self, "pipelineCdkPython",
                                         synth_action=synth_action,
                                         source_action=source_action,
                                         cloud_assembly_artifact=cloud_assembly_artifact)

        pprod_env = core.Environment(account="927534600513", region="eu-central-1")
        # pprod_props = core.StageProps(env=pprod_env)
        pipeline_stage_pprod = PipelineStage(self, id="preprod", env=pprod_env)
        pipeline.add_application_stage(pipeline_stage_pprod)