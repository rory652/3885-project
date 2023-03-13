import json, boto3
from boto3.dynamodb.conditions import Key
from secrets import token_hex

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('locations')
residents = dynamodb.Table('residents')


def generateItem(carehome, id, moduleId, location, residentId):
    return {
        'carehome': carehome,
        'id': id,
        'moduleId': moduleId,
        'location': location,
        'resident': residentId
    }


def lambda_handler(event, context):
    carehome = event["pathParameters"]["carehomeId"]

    if not isinstance(carehome, str):
        carehome = str(carehome)

    try:
        body = event["body"]
        if isinstance(body, str):
            body = json.loads(body)

        moduleId = body["moduleId"]
        location = body["location"]
        wearableId = body["wearable"]
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
    if not (residentId := getResident(carehome, wearableId)):
        return {
            'statusCode': 400,
            'headers': {},
            'body': json.dumps({
                'error': f'wearable {wearableId} not found'
            }),
            "isBase64Encoded": False,
        }

    locationId = generateId(carehome)

    response = table.put_item(Item=generateItem(carehome, locationId, moduleId, location, residentId))

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

    return generated


def getResident(carehome, wearable):
    response = residents.query(
        KeyConditionExpression=Key('carehome').eq(carehome)
    )

    if "Items" in response:
        for resident in response["Items"]:
            if resident["wearableId"] == wearable:
                return resident["id"]

    return False
