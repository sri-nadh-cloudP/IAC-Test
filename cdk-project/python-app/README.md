# Python CDK App

This is a Python CDK application that creates AWS infrastructure including:
- 2 EC2 instances (t3.micro and t3.small) with EBS volumes
- 2 S3 buckets with lifecycle policies (transition to Glacier after 30 days, expire after 365 days)
- 1 RDS MySQL instance
- VPC with public and private subnets
- Security groups for EC2 and RDS

## Setup

1. Create a virtual environment:
```bash
python3 -m venv .venv
```

2. Activate the virtual environment:
```bash
source .venv/bin/activate  # On macOS/Linux
# .venv\Scripts\activate.bat  # On Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Useful Commands

* `cdk ls`          list all stacks in the app
* `cdk synth`       emits the synthesized CloudFormation template
* `cdk deploy`      deploy this stack to your default AWS account/region
* `cdk diff`        compare deployed stack with current state
* `cdk destroy`     remove the stack from your AWS account

## Prerequisites

- AWS CLI configured with credentials
- Python 3.7 or later
- Node.js (for CDK CLI)
- AWS CDK CLI: `npm install -g aws-cdk`

## Deploy

```bash
cdk deploy
```

