import json, boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('residents')


def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'headers': {
            "Access-Control-Allow-Origin": "*"
        },
        'body': json.dumps({
            'residents': fetchResidents(event["pathParameters"]["carehome-id"])
        }),
        "isBase64Encoded": False,
    }


def fetchResidents(carehome):
    response = table.query(
        KeyConditionExpression=Key('carehome').eq(carehome)
    )

    return response["Items"]
