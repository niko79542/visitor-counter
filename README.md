### Live Frontend

[Live](niko-skoularikis.link) 
[Code](github.com/niko79542/resume)

### View Counter API

We will use Lambda, API Gateway, and dynamodb in order to build a simple serverless view counter for our resume website. 

### What is Lambda?  API Gateway? dynamodb?

dynamodb is a NoSQL flavor by AWS that is a fully managed, highly available distributed database.  You can scale up and down easily.

Lambda is a way to setup serverless functions without having to manage or provision servers.  We can use Lambda to express what shape of data we'd like to retrieve from Dynamo.

API Gateway provides a proxy we can use to accept API calls, integrate services we'd like to use to fufill them, and then return an appropriate result.  It also provides us testing and modeling tools.  

### API Gateway setup

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

At the top of [serverless.yml](serverless.yml) you can name your api service, specify the language to use at runtime, envionment, and AWS region to use.  You can also designate an IAM role for actions the serverless functions will be able to perform.  Here we specify actions for our dynamodb table, for our resource.  

All of these options can be also setup in the AWS console under lambda/API Gateway, but it may be faster to use the CLI once you are more comfortable.  

```yaml
functions:
  get:
    handler: handler.get
    events:
      - http:
          path: get_views
          method: get
  update:
    handler: handler.update
    events:
      - http:
          path: put_view
          method: put
```

Next, you can name the functions you'd like to use, along with their path and http method.  notice that the handler references the lambda function that will proxy the incoming http requests.  `handler.get` corresponds to the `get` function in [handler.py](handler.py)

### Setup your request handlers 

First connect the Python SDK for AWS.  This assumes you already have yoru [AWS Cli installed and configured](https://lmgtfy.app/?q=install+aws+cli).  

```py 
import boto3
dynamodb = boto3.client("dynamodb")
```

In [handler.py](handler.py) we can define our request handlers, for example this one is for `get`.

```py
def get(event, context):
    print(event)
    # Set the default error response
    response = {
        "statusCode": 500,
        "body": "An error occured while getting view."
    }

    view_query = dynamodb.get_item(
        TableName=table_name, Key={"id": {"N": "1"}})
```

Notice that the `event` object is intercepted by API Gateway.  We can use `print(event)` in combination with AWS Cloudfront to look at logs for what our request object looks like.  This is under Cloudwatch > Log Groups > #{Lambda function name} > #{Log Stream}.  Each request will create a new log stream.  We can any request data such as query parameters to generate queries to hit our dynamodb table.

![](https://res.cloudinary.com/dlpclqzwk/image/upload/v1653678269/Screenshot_from_2022-05-27_15-03-17_rjsvff.png)

### Get Data from dynamodb 

Notice that Dynamo expects queries to be formatted in JSON, with values as a Dict that have a Key which denotes the variable type.  I used [dynamo.py](dynamo.py) as a tool to convert back and forth between Dynamo supported JSON objects.  You can see the valid types here, or google `supported dynanmoDb Types python`.

```py
table_name = "views"

view_query = dynamodb.get_item(
    TableName=table_name, Key={"id": {"N": "1"}})
```

### Allow CORS 

Since we are planning to hit our API from an external server, we need to enable CORS (Cross origin resource sharing).  Include the following headers in your API response ensuring to allow the correct API methods (GET, POST, PUT, etc...)

```py
            "headers": {
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS,GET"
            },
```

Also allow preflight requests by adding `cors: true` to each of your lambda functions in the `serverless.yml`.


### Deploy to AWS 

Here are instructions to deploy to AWS.

```bash
$ sls deploy
```

### Run python unittest

```bash
$ python -m unittest discover -p "*.py" > results.txt
```


