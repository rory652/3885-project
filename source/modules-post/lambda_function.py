import json, boto3
from boto3.dynamodb.conditions import Key
from secrets import token_hex
from hashlib import sha256

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('modules')

standardHeaders = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Request-Headers": "SESSION-ID"
}


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
            'headers': {
                "Access-Control-Allow-Origin": "*"
            },
            'body': json.dumps({
                'error': f'{str(err)} field missing'
            }),
            "isBase64Encoded": False,
        }
    except ValueError as err:
        return {
            'statusCode': 400,
            'headers': standardHeaders,
            'body': json.dumps({
                'error': f'{str(err)}'
            }),
            "isBase64Encoded": False,
        }

    # Validate inputs here

    moduleId, hash = generateId(carehome)

    response = table.put_item(Item=generateItem(carehome, hash, room, status))

    return {
        'statusCode': 201,
        'headers': standardHeaders,
        'body': json.dumps({
            'database-status': response["ResponseMetadata"]["HTTPStatusCode"],
            'module-id': moduleId
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

    return generated, sha256(generated.encode()).hexdigest()
