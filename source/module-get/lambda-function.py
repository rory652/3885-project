import json, boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('modules')


def lambda_handler(event, context):
    path = event["pathParameters"]
    return {
        'statusCode': 200,
        'headers': {},
        'body': json.dumps({
            'modules': fetch(path["carehomeId"], path["moduleId"])
        }),
        "isBase64Encoded": False,
    }


def fetch(carehome, moduleId):
    response = table.query(
        KeyConditionExpression=Key('carehome').eq(carehome) & Key('id').eq(moduleId)
    )

    return response["Items"]
