import json, boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('contacts')

standardHeaders = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Request-Headers": "SESSION-ID"
}


def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'headers': standardHeaders,
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
