import json, boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('residents')


def lambda_handler(event, context):
    path = event["pathParameters"]
    return {
        'statusCode': 200,
        'headers': {},
        'body': json.dumps({
            'modules': fetch(path["carehome-id"], path["resident-id"])
        }),
        "isBase64Encoded": False,
    }


def fetch(carehome, residentId):
    response = table.query(
        KeyConditionExpression=Key('carehome').eq(carehome) & Key('id').eq(residentId)
    )

    return response["Items"]
