import json, boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('residents')

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
            'resident': fetch(path["carehome-id"], path["resident-id"])
        }),
        "isBase64Encoded": False,
    }


def fetch(carehome, residentId):
    response = table.query(
        KeyConditionExpression=Key('carehome').eq(carehome) & Key('id').eq(residentId)
    )

    return response["Items"]
