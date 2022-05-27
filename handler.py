import json
import boto3
import datetime
import dynamo

dynamodb = boto3.client("dynamodb")
table_name = "views"

def get(event, context):
    print(event)
    # Set the default error response
    response = {
        "statusCode": 500,
        "body": "An error occured while getting view."
    }

    view_query = dynamodb.get_item(
        TableName=table_name, Key={"id": {"N": "1"}})

    if "Item" in view_query:
        view = view_query["Item"]
        print(view)
        response = {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS,GET"
            },
            "body": json.dumps(dynamo.to_dict(view))
        }

    return response


def update(event, context):
    print(event)

    response = {
        "statusCode": 500,
        "body": f"An error occured while updating view"
    }
    
    res = dynamodb.update_item(
        TableName=table_name,
        Key={
            "id": {"N": "1"}
        },
        UpdateExpression="SET #views = if_not_exists(#views, :init) + :inc",
        ExpressionAttributeNames={
            "#views": "views"
        },
        ExpressionAttributeValues={
            ":inc": {"N": "1"},
            ":init": {"N": "0"}
        }
    )

    if res["ResponseMetadata"]["HTTPStatusCode"] == 200:
        response = {
            "statusCode": 201,
            "headers": {
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS,PUT"
            },
        }

    return response