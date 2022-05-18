import json
import logging
import boto3
import datetime
import dynamo

logger = logging.getLogger()
logger.setLevel(logging.INFO)
dynamodb = boto3.client('dynamodb')
table_name = 'posts'


def create(event, context):
    logger.info(f'Incoming request is: {event}')

    # Set the default error response
    response = {
        "statusCode": 500,
        "body": "An error occured while creating post."
    }

    post_str = event['body']
    post = json.loads(post_str)
    current_timestamp = datetime.datetime.now().isoformat()
    post['createdAt'] = current_timestamp

    res = dynamodb.put_item(
        TableName=table_name, Item=dynamo.to_item(post))

    # If creation is successful
    if res['ResponseMetadata']['HTTPStatusCode'] == 200:
        response = {
            "statusCode": 201,
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST'
            },
        }

    return response


def get(event, context):
    logger.info(f'Incoming request is: {event}')
    # Set the default error response
    response = {
        "statusCode": 500,
        "body": "An error occured while getting post."
    }

    post_id = event['pathParameters']['postId']

    post_query = dynamodb.get_item(
        TableName=table_name, Key={'id': {'N': post_id}})

    if 'Item' in post_query:
        post = post_query['Item']
        logger.info(f'Post is: {post}')
        response = {
            "statusCode": 200,
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,GET'
            },
            "body": json.dumps(dynamo.to_dict(post))
        }

    return response


def all(event, context):
    logger.info(f'Incoming request is: {event}')

    # Set the default error response
    response = {
        "statusCode": 500,
        "body": "An error occured while getting all posts."
    }

    scan_result = dynamodb.scan(TableName=table_name)['Items']

    posts = []

    for item in scan_result:
        posts.append(dynamo.to_dict(item))

    response = {
        "statusCode": 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,GET'
        },
        "body": json.dumps(posts)
    }

    return response


def update(event, context):
    logger.info(f'Incoming request is: {event}')

    post_id = event['pathParameters']['postId']

    response = {
        "statusCode": 500,
        "body": f"An error occured while updating post {post_id}"
    }

    post_str = event['body']

    post = json.loads(post_str)

    res = dynamodb.update_item(
        TableName=table_name,
        Key={
            'id': {'N': post_id}
        },
        UpdateExpression="set content=:c, author=:a, updatedAt=:u",
        ExpressionAttributeValues={
            ':c': dynamo.to_item(post['content']),
            ':a': dynamo.to_item(post['author']),
            ':u': dynamo.to_item(datetime.datetime.now().isoformat())
        },
        ReturnValues="UPDATED_NEW"
    )

    # If updation is successful for post
    if res['ResponseMetadata']['HTTPStatusCode'] == 200:
        response = {
            "statusCode": 200,
        }

    return response


def delete(event, context):
    logger.info(f'Incoming request is: {event}')

    post_id = event['pathParameters']['postId']

    # Set the default error response
    response = {
        "statusCode": 500,
        "body": f"An error occured while deleting post {post_id}"
    }

    res = dynamodb.delete_item(TableName=table_name, Key={
                               'id': {'N': post_id}})

    # If deletion is successful for post
    if res['ResponseMetadata']['HTTPStatusCode'] == 200:
        response = {
            "statusCode": 204,
        }
    return response