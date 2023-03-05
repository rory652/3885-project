import json, boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('sessions')


def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'headers': {},
        'body': json.dumps({
            'database-status': delete(event["headers"]["SESSION-ID"])["ResponseMetadata"]["HTTPStatusCode"]
        }),
        "isBase64Encoded": False,
    }


def delete(session):
    response = table.delete_item(
        Key={
            'id': session,
        }
    )

    return response
