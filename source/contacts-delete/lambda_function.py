import json, boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('contacts')


def lambda_handler(event, context):
    path = event["pathParameters"]
    return {
        'statusCode': 200,
        'headers': {},
        'body': json.dumps({
            'database-status': delete(path["carehomeId"], path["contactId"])["ResponseMetadata"]["HTTPStatusCode"]
        }),
        "isBase64Encoded": False,
    }


def delete(carehome, id):
    response = table.delete_item(
        Key={
            'carehome': carehome,
            'id': id
        }
    )

    return response