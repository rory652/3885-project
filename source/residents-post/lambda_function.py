import json, boto3
from boto3.dynamodb.conditions import Key
from secrets import token_hex

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('residents')

standardHeaders = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Request-Headers": "SESSION-ID"
}


def generateItem(carehome, id, name, status, wearable):
    return {
        'carehome': carehome,
        'id': id,
        'name': name,
        'status': status,
        'wearableId': wearable,
    }


def lambda_handler(event, context):
    carehome = event["pathParameters"]["carehome-id"]

    if not isinstance(carehome, str):
        carehome = str(carehome)

    try:
        body = event["body"]
        if isinstance(body, str):
            body = json.loads(body)

        name = body["name"]
        status = body["status"]
        wearable = body["wearableId"]
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

    if name == "":
        return {
            'statusCode': 400,
            'headers': {
                "Access-Control-Allow-Origin": "*"
            },
            'body': json.dumps({
                'error': f'name not set'
            }),
            "isBase64Encoded": False,
        }

    if wearable == "":
        return {
            'statusCode': 400,
            'headers': {
                "Access-Control-Allow-Origin": "*"
            },
            'body': json.dumps({
                'error': f'wearable not set'
            }),
            "isBase64Encoded": False,
        }

    residentId = generateId(carehome)

    response = table.put_item(Item=generateItem(carehome, residentId, name, status, wearable))

    return {
        'statusCode': 201,
        'headers': standardHeaders,
        'body': json.dumps({
            'database-status': response["ResponseMetadata"]["HTTPStatusCode"],
            'resident-id': residentId
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

    return generated
