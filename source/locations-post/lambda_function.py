import json, boto3, time
from boto3.dynamodb.conditions import Key
from decimal import Decimal
from hashlib import sha256

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('locations')
residents = dynamodb.Table('residents')
modules = dynamodb.Table('modules')

standardHeaders = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Request-Headers": "MODULE-ID"
}


def generateItem(carehome, utc, module, location, residentId):
    return json.loads(json.dumps({
        'carehome': carehome,
        'time': utc,
        'module': module,
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

        moduleId = event["headers"]["module-id"]
        location = body["location"]
        wearableId = body["wearable"]
    except KeyError as err:
        return {
            'statusCode': 400,
            'headers': standardHeaders,
            'body': json.dumps({
                'error': f'{str(err)} field missing'
            }),
            "isBase64Encoded": False,
        }

    try:
        location["X"] = float(location["X"])
        location["Y"] = float(location["Y"])
        location["Z"] = float(location["Z"])
        print(location)
    except KeyError as err:
        return {
            'statusCode': 400,
            'headers': standardHeaders,
            'body': json.dumps({
                'error': f'incorrect location: {str(err)} field missing'
            }),
            "isBase64Encoded": False,
        }

    # Validate inputs here
    if not (residentId := getResident(carehome, wearableId)):
        return {
            'statusCode': 400,
            'headers': standardHeaders,
            'body': json.dumps({
                'error': f'wearable {wearableId} not found'
            }),
            "isBase64Encoded": False,
        }

    if not checkModule(carehome, moduleId):
        return {
            'statusCode': 400,
            'headers': standardHeaders,
            'body': json.dumps({
                'error': f'module {moduleId} not found'
            }),
            "isBase64Encoded": False,
        }

    response = table.put_item(Item=generateItem(carehome, timestamp(), moduleId, location, residentId))

    return {
        'statusCode': 201,
        'headers': standardHeaders,
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


def checkModule(carehome, module):
    hash = sha256(module.encode()).hexdigest()

    response = modules.query(
        KeyConditionExpression=Key('carehome').eq(carehome) & Key('id').eq(hash)
    )

    return len(response["Items"]) > 0
