from aws_cdk import (
    Stack,
    Tags,
    aws_ec2 as ec2,
    aws_s3 as s3,
    aws_rds as rds,
    RemovalPolicy,
    Duration,
)
from constructs import Construct

class PythonAppStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create VPC for EC2 and RDS
        vpc = ec2.Vpc(self, "PythonAppVPC",
            max_azs=2,
            nat_gateways=1,
        )
        Tags.of(vpc).add("Name", "Python-App-VPC")

        # Create Security Group for EC2
        ec2_security_group = ec2.SecurityGroup(self, "EC2SecurityGroup",
            vpc=vpc,
            description="Security group for EC2 instances",
            allow_all_outbound=True,
        )
        Tags.of(ec2_security_group).add("Name", "Python-EC2-SG")

        # Create EC2 Instance 1
        ec2_instance_1 = ec2.Instance(self, "EC2Instance1",
            vpc=vpc,
            instance_type=ec2.InstanceType("t3.micro"),
            machine_image=ec2.MachineImage.latest_amazon_linux2(),
            security_group=ec2_security_group,
            block_devices=[
                ec2.BlockDevice(
                    device_name="/dev/sda1",
                    volume=ec2.BlockDeviceVolume.ebs(
                        volume_size=50,
                        volume_type=ec2.EbsDeviceVolumeType.GP3,
                    )
                )
            ],
        )
        Tags.of(ec2_instance_1).add("Name", "EC2-Instance-1")

        # Create EC2 Instance 2
        ec2_instance_2 = ec2.Instance(self, "EC2Instance2",
            vpc=vpc,
            instance_type=ec2.InstanceType("t3.small"),
            machine_image=ec2.MachineImage.latest_amazon_linux2(),
            security_group=ec2_security_group,
            block_devices=[
                ec2.BlockDevice(
                    device_name="/dev/sda1",
                    volume=ec2.BlockDeviceVolume.ebs(
                        volume_size=40,
                        volume_type=ec2.EbsDeviceVolumeType.GP3,
                    )
                )
            ],
        )
        Tags.of(ec2_instance_2).add("Name", "EC2-Instance-2")

        # Create S3 Bucket 1 with lifecycle rules
        s3_bucket_1 = s3.Bucket(self, "S3Bucket1",
            bucket_name=None,  # Auto-generate unique name
            lifecycle_rules=[
                s3.LifecycleRule(
                    id="TransitionToGlacier",
                    enabled=True,
                    transitions=[
                        s3.Transition(
                            storage_class=s3.StorageClass.GLACIER,
                            transition_after=Duration.days(30)
                        )
                    ],
                    expiration=Duration.days(365)
                )
            ],
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )
        Tags.of(s3_bucket_1).add("Name", "Python-S3-Bucket-1")

        # Create S3 Bucket 2 with lifecycle rules
        s3_bucket_2 = s3.Bucket(self, "S3Bucket2",
            bucket_name=None,  # Auto-generate unique name
            lifecycle_rules=[
                s3.LifecycleRule(
                    id="TransitionToGlacier",
                    enabled=True,
                    transitions=[
                        s3.Transition(
                            storage_class=s3.StorageClass.GLACIER,
                            transition_after=Duration.days(30)
                        )
                    ],
                    expiration=Duration.days(365)
                )
            ],
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )
        Tags.of(s3_bucket_2).add("Name", "Python-S3-Bucket-2")

        # Create Security Group for RDS
        rds_security_group = ec2.SecurityGroup(self, "RDSSecurityGroup",
            vpc=vpc,
            description="Security group for RDS instance",
            allow_all_outbound=True,
        )
        rds_security_group.add_ingress_rule(
            peer=ec2_security_group,
            connection=ec2.Port.tcp(3306),
            description="Allow MySQL access from EC2 instances",
        )
        Tags.of(rds_security_group).add("Name", "Python-RDS-SG")

        # Create RDS Instance
        rds_instance = rds.DatabaseInstance(self, "RDSInstance",
            engine=rds.DatabaseInstanceEngine.mysql(
                version=rds.MysqlEngineVersion.VER_8_0_35
            ),
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.BURSTABLE3,
                ec2.InstanceSize.MICRO
            ),
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS
            ),
            security_groups=[rds_security_group],
            multi_az=False,
            allocated_storage=20,
            storage_type=rds.StorageType.GP3,
            deletion_protection=False,
            removal_policy=RemovalPolicy.DESTROY,
            database_name="mydb",
        )
        Tags.of(rds_instance).add("Name", "Python-RDS-Instance")

