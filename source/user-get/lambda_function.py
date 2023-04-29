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
        'statusCode': 200,
        'headers': standardHeaders,
        'body': json.dumps({
            'user': fetch(path["carehome-id"], path["username"])
        }),
        "isBase64Encoded": False,
    }


def fetch(carehome, username):
    response = table.query(
        KeyConditionExpression=Key('carehome').eq(carehome) & Key('username').eq(username)
    )

    return {key: response["Items"][0][key] for key in ["username", "carehome", "role"]}
