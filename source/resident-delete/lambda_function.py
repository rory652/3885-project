import json, boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('residents')


def lambda_handler(event, context):
    path = event["pathParameters"]
    return {
        'statusCode': 200,
        'headers': {
            "Access-Control-Allow-Origin": "*"
        },
        'body': json.dumps({
            'database-status': delete(path["carehome-id"], path["resident-id"])["ResponseMetadata"]["HTTPStatusCode"]
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
