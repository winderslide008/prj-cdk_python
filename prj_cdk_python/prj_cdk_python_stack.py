from aws_cdk import (
    core,
    aws_ec2 as ec2,
    aws_iam as iam,
    aws_ssm as ssm,
)

from prj_cdk_python.prj_cdk_python_nested_stack import LambdaCronNestedStack


class PrjCdkPythonStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # The code that defines your stack goes here

        # VPC
        vpc = ec2.Vpc(self, "VPC", nat_gateways=0, subnet_configuration=[ec2.SubnetConfiguration(
            name="public",
            subnet_type=ec2.SubnetType.PUBLIC
        )])

        # AMI
        amzn_linux = ec2.MachineImage.latest_amazon_linux()

        # Instance role and SSM Managed Policy
        role = iam.Role(self, "InstanceSSM", assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"))
        role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AmazonEC2RoleforSSM"))

        # Security Group
        sg = ec2.SecurityGroup(self, "SG",
                               vpc=vpc,
                               description="allow ssh and http",
                               allow_all_outbound=True,
                               security_group_name="SecurityGroupName")

        my_peer = ec2.Peer.prefix_list("pl-1ea54077")
        ssh_port = ec2.Port.tcp(22)
        all_peer = ec2.Peer.ipv4("0.0.0.0/0")
        http_port = ec2.Port.tcp(80)

        sg.add_ingress_rule(my_peer, ssh_port)
        sg.add_ingress_rule(all_peer, http_port)

        # Userdata to install nginx
        user_data = ec2.UserData.for_linux()
        user_data.add_commands("yum install -y nginx", "chkconfig nginx on", "service nginx start")

        # SSM
        env = "Preprod"
        company_param_name = "/Config/" + env + "/CompanyName"
        company_param = ssm.StringParameter(self, id="Parameter",
                                            allowed_pattern='.*',
                                            description="The name of the company",
                                            string_value="MyAWSomeCompany",
                                            tier=ssm.ParameterTier.STANDARD)

        # Instance
        instance = ec2.Instance(self, "Instance",
                                instance_type=ec2.InstanceType("t3a.nano"),
                                machine_image=amzn_linux,
                                vpc=vpc,
                                key_name="paandrie",
                                security_group=sg,
                                role=role,
                                user_data=user_data
                                )
        # Nested stack
        LambdaCronNestedStack(self, "not:a:stack:name")
