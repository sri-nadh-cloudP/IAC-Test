# CDK Multi-Language Project

This project contains two separate CDK applications demonstrating Infrastructure as Code (IaC) in different programming languages:

1. **Python CDK App** (`python-app/`) - Python implementation
2. **JavaScript CDK App** (`javascript-app/`) - JavaScript implementation

Both applications create identical AWS infrastructure with the same tags as defined in the CloudFormation template.

## Infrastructure Components

Each CDK app creates:

### EC2 Instances
- **EC2 Instance 1**: t3.micro with 50GB GP3 EBS volume
- **EC2 Instance 2**: t3.small with 40GB GP3 EBS volume

### S3 Buckets
- **S3 Bucket 1**: With lifecycle rules (Glacier transition after 30 days, expiration after 365 days)
- **S3 Bucket 2**: With lifecycle rules (Glacier transition after 30 days, expiration after 365 days)

### RDS Database
- **RDS Instance**: MySQL 8.0.35, db.t3.micro, 20GB GP3 storage
- Located in private subnet with proper security group configuration
- Database name: `mydb`

### Networking
- **VPC**: Custom VPC with 2 Availability Zones
- **Subnets**: Public and private subnets
- **NAT Gateway**: For private subnet internet access
- **Security Groups**: 
  - EC2 Security Group (allows outbound traffic)
  - RDS Security Group (allows MySQL access from EC2 instances)

## Tagging Strategy

All resources are tagged with `Name` tags following the pattern from the CloudFormation template:
- EC2 instances: `EC2-Instance-1`, `EC2-Instance-2`
- S3 buckets: `[Language]-S3-Bucket-1`, `[Language]-S3-Bucket-2`
- RDS instance: `[Language]-RDS-Instance`
- VPC and Security Groups: Appropriately named

## Prerequisites

### For Both Apps
- AWS CLI configured with appropriate credentials
- AWS CDK CLI installed: `npm install -g aws-cdk`
- Valid AWS account with necessary permissions

### For Python App
- Python 3.7 or later
- pip (Python package manager)

### For JavaScript App
- Node.js 14.x or later
- npm (Node package manager)

## Getting Started

### Python App

```bash
cd python-app

# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # On macOS/Linux
# .venv\Scripts\activate.bat  # On Windows

# Install dependencies
pip install -r requirements.txt

# Bootstrap CDK (first time only)
cdk bootstrap

# Deploy the stack
cdk deploy
```

### JavaScript App

```bash
cd javascript-app

# Install dependencies
npm install

# Bootstrap CDK (first time only)
cdk bootstrap

# Deploy the stack
cdk deploy
```

## Useful CDK Commands

Both apps support these CDK commands:

- `cdk ls` - List all stacks in the app
- `cdk synth` - Synthesize CloudFormation template
- `cdk deploy` - Deploy the stack to AWS
- `cdk diff` - Show differences between deployed stack and current code
- `cdk destroy` - Remove the stack from AWS

## Cost Considerations

The infrastructure created by these apps will incur AWS costs:
- EC2 instances (t3.micro and t3.small)
- RDS database instance (db.t3.micro)
- NAT Gateway (highest cost item)
- S3 storage and data transfer
- EBS volumes

Remember to run `cdk destroy` when you're done testing to avoid unnecessary charges.

## Project Structure

```
cdk-project/
├── python-app/
│   ├── app.py                      # Python CDK app entry point
│   ├── cdk.json                    # CDK configuration
│   ├── requirements.txt            # Python dependencies
│   ├── README.md                   # Python app documentation
│   └── python_app/
│       ├── __init__.py
│       └── python_app_stack.py     # Python stack definition
│
├── javascript-app/
│   ├── bin/
│   │   └── javascript-app.js       # JavaScript CDK app entry point
│   ├── lib/
│   │   └── javascript-app-stack.js # JavaScript stack definition
│   ├── cdk.json                    # CDK configuration
│   ├── package.json                # Node.js dependencies
│   └── README.md                   # JavaScript app documentation
│
└── README.md                       # This file
```

## Security Notes

1. The RDS instance is created in a private subnet and is only accessible from EC2 instances
2. RDS master password is auto-generated and stored in AWS Secrets Manager
3. Security groups follow the principle of least privilege
4. For production use, consider:
   - Enabling RDS encryption
   - Enabling S3 bucket encryption
   - Enabling deletion protection for RDS
   - Using more restrictive security group rules
   - Enabling multi-AZ for RDS for high availability

## Troubleshooting

### Python App Issues
- Ensure virtual environment is activated
- Check Python version: `python3 --version`
- Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`

### JavaScript App Issues
- Clear npm cache: `npm cache clean --force`
- Remove node_modules and reinstall: `rm -rf node_modules && npm install`
- Check Node.js version: `node --version`

### CDK Issues
- Update CDK CLI: `npm update -g aws-cdk`
- Bootstrap again if needed: `cdk bootstrap`
- Check AWS credentials: `aws sts get-caller-identity`

## License

This project is provided as-is for educational and demonstration purposes.

