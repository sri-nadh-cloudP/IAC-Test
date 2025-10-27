const { Stack, Tags, RemovalPolicy, Duration } = require('aws-cdk-lib');
const ec2 = require('aws-cdk-lib/aws-ec2');
const s3 = require('aws-cdk-lib/aws-s3');
const rds = require('aws-cdk-lib/aws-rds');

class JavascriptAppStack extends Stack {
  constructor(scope, id, props) {
    super(scope, id, props);

    // Create VPC for EC2 and RDS
    const vpc = new ec2.Vpc(this, 'JavascriptAppVPC', {
      maxAzs: 2,
      natGateways: 1,
    });
    Tags.of(vpc).add('Name', 'Javascript-App-VPC');

    // Create Security Group for EC2
    const ec2SecurityGroup = new ec2.SecurityGroup(this, 'EC2SecurityGroup', {
      vpc: vpc,
      description: 'Security group for EC2 instances',
      allowAllOutbound: true,
    });
    Tags.of(ec2SecurityGroup).add('Name', 'Javascript-EC2-SG');

    // Create EC2 Instance 1
    const ec2Instance1 = new ec2.Instance(this, 'EC2Instance1', {
      vpc: vpc,
      instanceType: new ec2.InstanceType('t3.micro'),
      machineImage: ec2.MachineImage.latestAmazonLinux2(),
      securityGroup: ec2SecurityGroup,
      blockDevices: [
        {
          deviceName: '/dev/sda1',
          volume: ec2.BlockDeviceVolume.ebs(60, {
            volumeType: ec2.EbsDeviceVolumeType.GP3,
          }),
        },
      ],
    });
    Tags.of(ec2Instance1).add('Name', 'EC2-Instance-1');

    // Create EC2 Instance 2
    const ec2Instance2 = new ec2.Instance(this, 'EC2Instance2', {
      vpc: vpc,
      instanceType: new ec2.InstanceType('t3.small'),
      machineImage: ec2.MachineImage.latestAmazonLinux2(),
      securityGroup: ec2SecurityGroup,
      blockDevices: [
        {
          deviceName: '/dev/sda1',
          volume: ec2.BlockDeviceVolume.ebs(40, {
            volumeType: ec2.EbsDeviceVolumeType.GP3,
          }),
        },
      ],
    });
    Tags.of(ec2Instance2).add('Name', 'EC2-Instance-2');

    // Create S3 Bucket 1 with lifecycle rules
    const s3Bucket1 = new s3.Bucket(this, 'S3Bucket1', {
      lifecycleRules: [
        {
          id: 'TransitionToGlacier',
          enabled: true,
          transitions: [
            {
              storageClass: s3.StorageClass.GLACIER,
              transitionAfter: Duration.days(30),
            },
          ],
          expiration: Duration.days(365),
        },
      ],
      removalPolicy: RemovalPolicy.DESTROY,
      autoDeleteObjects: true,
    });
    Tags.of(s3Bucket1).add('Name', 'Javascript-S3-Bucket-1');

    // Create S3 Bucket 2 with lifecycle rules
    const s3Bucket2 = new s3.Bucket(this, 'S3Bucket2', {
      lifecycleRules: [
        {
          id: 'TransitionToGlacier',
          enabled: true,
          transitions: [
            {
              storageClass: s3.StorageClass.GLACIER,
              transitionAfter: Duration.days(30),
            },
          ],
          expiration: Duration.days(365),
        },
      ],
      removalPolicy: RemovalPolicy.DESTROY,
      autoDeleteObjects: true,
    });
    Tags.of(s3Bucket2).add('Name', 'Javascript-S3-Bucket-2');

    // Create Security Group for RDS
    const rdsSecurityGroup = new ec2.SecurityGroup(this, 'RDSSecurityGroup', {
      vpc: vpc,
      description: 'Security group for RDS instance',
      allowAllOutbound: true,
    });
    rdsSecurityGroup.addIngressRule(
      ec2SecurityGroup,
      ec2.Port.tcp(3306),
      'Allow MySQL access from EC2 instances'
    );
    Tags.of(rdsSecurityGroup).add('Name', 'Javascript-RDS-SG');

    // Create RDS Instance
    const rdsInstance = new rds.DatabaseInstance(this, 'RDSInstance', {
      engine: rds.DatabaseInstanceEngine.mysql({
        version: rds.MysqlEngineVersion.VER_8_0_35,
      }),
      instanceType: ec2.InstanceType.of(
        ec2.InstanceClass.BURSTABLE3,
        ec2.InstanceSize.MICRO
      ),
      vpc: vpc,
      vpcSubnets: {
        subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS,
      },
      securityGroups: [rdsSecurityGroup],
      multiAz: false,
      allocatedStorage: 20,
      storageType: rds.StorageType.GP3,
      deletionProtection: false,
      removalPolicy: RemovalPolicy.DESTROY,
      databaseName: 'mydb',
    });
    Tags.of(rdsInstance).add('Name', 'Javascript-RDS-Instance');
  }
}

module.exports = { JavascriptAppStack };

