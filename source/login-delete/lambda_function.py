import json, boto3
from boto3.dynamodb.conditions import Key
from hashlib import sha256
from secrets import token_hex

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('sessions')
users = dynamodb.Table('users')


def generateItem(carehome, session, username, role):
    return {
        'carehome': carehome,
        'id': session,
        'username': username,
        'role': role,
    }


def generateResponse(status, body, headers=None):
    if headers is None:
        headers = {}
    return {
        'statusCode': status,
        'headers': headers,
        'body': json.dumps(body),
        "isBase64Encoded": False,
    }


def lambda_handler(event, context):
    carehome = event["pathParameters"]["carehomeId"]

    if not isinstance(carehome, str):
        carehome = str(carehome)

    try:
        headers = event["headers"]
        if isinstance(headers, str):
            headers = json.loads(headers)

        session = headers["SESSION-ID"]
    except KeyError as err:
        return generateResponse(400, {'error': f'{str(err)} field missing'})

    return generateResponse(204, {'database-status': delete(carehome, session)["ResponseMetadata"]["HTTPStatusCode"]})


def delete(carehome, session):
    response = table.delete_item(
        Key={
            'carehome': carehome,
            'id': session
        }
    )

    return response
