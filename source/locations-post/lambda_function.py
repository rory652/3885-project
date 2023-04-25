import json, boto3, time
from boto3.dynamodb.conditions import Key
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('locations')
residents = dynamodb.Table('residents')


def generateItem(carehome, utc, moduleId, location, residentId):
    return json.loads(json.dumps({
        'carehome': carehome,
        'time': utc,
        'moduleId': moduleId,
        'location': location,
        'resident': residentId
    }), parse_float=Decimal)


def lambda_handler(event, context):
    carehome = event["pathParameters"]["carehome-id"]

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

    response = table.put_item(Item=generateItem(carehome, timestamp(), moduleId, location, residentId))

    return {
        'statusCode': 201,
        'headers': {},
        'body': json.dumps({
            'database-status': response["ResponseMetadata"]["HTTPStatusCode"]
        }),
        "isBase64Encoded": False,
    }


def timestamp():
    return time.time()


def getResident(carehome, wearable):
    response = residents.query(
        KeyConditionExpression=Key('carehome').eq(carehome)
    )

    if "Items" in response:
        for resident in response["Items"]:
            if resident["wearableId"] == wearable:
                return resident["id"]

    return False
