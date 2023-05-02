import json, boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('users')

standardHeaders = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Request-Headers": "SESSION-ID"
}


def lambda_handler(event, context):
    path = event["pathParameters"]
    return {
        'statusCode': 204,
        'headers': standardHeaders,
        'body': json.dumps({
            'database-status': delete(path["carehome-id"], path["username"])["ResponseMetadata"]["HTTPStatusCode"]
        }),
        "isBase64Encoded": False,
    }


def delete(carehome, username):
    response = table.delete_item(
        Key={
            'carehome': carehome,
            'username': username
        }
    )

    return response
