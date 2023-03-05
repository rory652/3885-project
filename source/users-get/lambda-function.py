import json, boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('users')


def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'headers': {},
        'body': json.dumps({
            'users': fetchUsers(event["pathParameters"]["carehomeId"])
        }),
        "isBase64Encoded": False,
    }


def fetchUsers(carehome):
    response = table.query(
        KeyConditionExpression=Key('carehome').eq(carehome)
    )

    return response["Items"]
