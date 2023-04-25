import json, boto3
from boto3.dynamodb.conditions import Key
from secrets import token_hex
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('contacts')
locationTable = dynamodb.Table('locations')

cutoffTime = 5  # maximum time between location to still be counted


def generateItem(carehome, id, location, resident):
    return {
        'carehome': carehome,
        'id': id,
        'count': location,
        'resident': resident
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
        location = {key: value["S"] for (key, value) in incoming["location"]["M"].items()}
        resident = incoming["resident"]["S"]
        module = incoming["moduleId"]["S"]
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

    contactId = generateId(carehome)

    response = table.put_item(Item=generateItem(carehome, contactId, len(locations), resident))

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
        KeyConditionExpression=Key('carehome').eq(carehome)
    )

    for i in response["Items"]:
        if i["moduleId"] == module and i["resident"] != resident:
            if abs(i["time"] - utc) < cutoffTime:
                collected.append(i)

    return collected


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
