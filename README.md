### What is Lambda?  API Gateway? DynamoDB?




[yaml](serverless.yml)
```yaml
service: views-api

provider:
  name: aws
  runtime: python3.8
  stage: dev
  region: us-west-1
  iamRoleStatements:
    - Effect: Allow
      Action:
        - dynamodb:Query
        - dynamodb:Scan
        - dynamodb:GetItem
        - dynamodb:PutItem
        - dynamodb:UpdateItem
        - dynamodb:DeleteItem
      Resource: "arn:aws:dynamodb:us-west-1:797377682706:table/views"
package:
  exclude:
    - node_modules/**
    - venv/**
```

At the top of [serverless.yml](serverless.yml) you can name your api service, specify the language to use at runtime, envionment, and AWS region to use.  You can also designate an IAM role for actions the serverless functions will be able to perform.  Here we specify actions for our DynamoDB table, for our resource.  

All of these options can be also setup in the AWS console under lambda/API Gateway, but it may be faster to use the CLI once you are more comfortable.  

### Deploy to AWS 

$ sls deploy 

