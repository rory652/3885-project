import json, boto3
from boto3.dynamodb.conditions import Key
from secrets import token_hex

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('contacts')


def generateItem(carehome, id, location, resident):
    return {
        'carehome': carehome,
        'id': id,
        'location': location,
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
    locationId = incoming["id"]["S"]

    try:
        location = {key: value["S"] for (key, value) in incoming["location"]["M"].items()}
        resident = incoming["resident"]["S"]
    except KeyError as err:
        return {
            'statusCode': 400,
            'headers': {},
            'body': json.dumps({
                'error': f'{str(err)} field missing'
            }),
            "isBase64Encoded": False,
        }

    contactId = generateId(carehome)

    response = table.put_item(Item=generateItem(carehome, contactId, location, resident))

    return {
        'statusCode': 200,
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