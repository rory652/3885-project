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
