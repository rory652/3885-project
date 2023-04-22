import json, boto3
from boto3.dynamodb.conditions import Key
from secrets import token_hex
from hashlib import sha256

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('modules')


def generateItem(carehome, id, room, status):
    return {
        'carehome': carehome,
        'id': id,
        'room': room,
        'status': status,
    }


def lambda_handler(event, context):
    carehome = event["pathParameters"]["carehome-id"]

    if not isinstance(carehome, str):
        carehome = str(carehome)

    try:
        body = event["body"]
        if isinstance(body, str):
            body = json.loads(body)

        room = body["room"]
        status = body["status"]
    except KeyError as err:
        return {
            'statusCode': 400,
            'headers': {},
            'body': json.dumps({
                'error': f'{str(err)} field missing'
            }),
            "isBase64Encoded": False,
        }

    # Validate inputs here

    moduleId = generateId(carehome)

    response = table.put_item(Item=generateItem(carehome, moduleId, room, status))

    return {
        'statusCode': 201,
        'headers': {},
        'body': json.dumps({
            'database-status': response["ResponseMetadata"]["HTTPStatusCode"]
        }),
        "isBase64Encoded": False,
    }


def generateId(carehome):
    valid = False
    generated = token_hex(8)

    while not valid:
        response = table.query(
            KeyConditionExpression=Key('carehome').eq(carehome) & Key('id').eq(generated)
        )

        if len(response["Items"]) == 0:
            valid = True
        else:
            generated = token_hex(8)

    return sha256(generated.encode()).hexdigest()
