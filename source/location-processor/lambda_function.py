import json, boto3
from boto3.dynamodb.conditions import Key
from secrets import token_hex
from decimal import Decimal
from math import sqrt

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('contacts')
locationTable = dynamodb.Table('locations')

CUTOFFTIME = 5  # maximum time between location to still be counted
MAXDISTANCE = 2


def generateItem(carehome, id, contacts):
    return {
        'carehome': carehome,
        'id': id,
        'contacts': contacts,
        'count': len(contacts)
    }


def lambda_handler(event, context):
    if event['Records'][0]["eventName"] != "INSERT":
        return {
            'statusCode': 200,
            'headers': {},
            'body': json.dumps({
                'message': "Unmonitored event"
            }),
            "isBase64Encoded": False,
        }

    incoming = event['Records'][0]["dynamodb"]["NewImage"]

    carehome = incoming["carehome"]["S"]
    timestamp = Decimal(incoming["time"]["N"])

    try:
        location = {key: Decimal(value["N"]) for (key, value) in incoming["location"]["M"].items()}
        resident = incoming["resident"]["S"]
        module = incoming["module"]["S"]
    except KeyError as err:
        return {
            'statusCode': 400,
            'headers': {},
            'body': json.dumps({
                'error': f'{str(err)} field missing'
            }),
            "isBase64Encoded": False,
        }

    locations = getLocations(carehome, timestamp, module, resident)
    contacts = checkLocations(location, resident, locations)

    contactId = generateId(carehome)

    response = table.put_item(Item=generateItem(carehome, contactId, contacts))

    return {
        'statusCode': 200,
        'headers': {},
        'body': json.dumps({
            'database-status': response["ResponseMetadata"]["HTTPStatusCode"]
        }),
        "isBase64Encoded": False,
    }


def getLocations(carehome, utc, module, resident):
    collected = []

    response = locationTable.query(
        KeyConditionExpression=Key('carehome').eq(carehome) & Key('time').between(utc - CUTOFFTIME, utc + CUTOFFTIME)
    )

    for i in response["Items"]:
        if i["module"] == module and i["resident"] != resident:
            collected.append(i)

    return collected


def checkLocations(location, resident, toCheck):
    print(location, resident)
    print(toCheck)
    valid = []

    for check in toCheck:
        if getDistance(location, check["location"]) < MAXDISTANCE:
            valid.append([resident, check["resident"]])

    return valid


def getDistance(locOne, locTwo):
    x = pow(locOne["X"] - locTwo["X"], 2)
    y = pow(locOne["Y"] - locTwo["Y"], 2)
    z = pow(locOne["Z"] - locTwo["Z"], 2)

    return sqrt(x + y + z)


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