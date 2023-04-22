import json, boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('contacts')


def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'headers': {},
        'body': json.dumps({
            'contacts': fetch(event["pathParameters"]["carehome-id"])
        }),
        "isBase64Encoded": False,
    }


def fetch(carehome):
    response = table.query(
        KeyConditionExpression=Key('carehome').eq(carehome)
    )

    return response["Items"]
