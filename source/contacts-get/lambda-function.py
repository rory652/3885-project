import json, boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('contacts')


def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'headers': {},
        'body': json.dumps({
            'contacts': fetchContacts(event["pathParameters"]["carehomeId"])
        }),
        "isBase64Encoded": False,
    }


def fetchContacts(carehome):
    response = table.query(
        KeyConditionExpression=Key('carehome').eq(carehome)
    )

    return response["Items"]
