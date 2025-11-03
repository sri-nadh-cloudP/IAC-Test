#!/usr/bin/env node

const cdk = require('aws-cdk-lib');
const { JavascriptAppStack } = require('../lib/javascript-app-stack');

const app = new cdk.App();
new JavascriptAppStack(app, 'JavascriptAppStack', {
  env: {
    account: process.env.CDK_DEFAULT_ACCOUNT,
    region: process.env.CDK_DEFAULT_REGION
  }
});
