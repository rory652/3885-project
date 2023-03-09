import json, boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('residents')


def generateKey(carehome, id):
    return {
        'carehome': carehome,
        'id': id,
    }


def generateAttributes(**attributes):
    update = {}

    for key, value in attributes.items():
        if value != "":
            update[key] = {"Value": value}

    return update


def lambda_handler(event, context):
    carehome = event["pathParameters"]["carehomeId"]

    if not isinstance(carehome, str):
        carehome = str(carehome)

    resident = event["pathParameters"]["residentId"]

    try:
        body = event["body"]
        if isinstance(body, str):
            body = json.loads(body)

        new_name = body["new_name"]
        new_status = body["new_status"]
        new_wearable = body["new_wearable"]
    except KeyError as err:
        return {
            'statusCode': 400,
            'headers': {},
            'body': json.dumps({
                'error': f'{str(err)} field missing - set to empty string to not update'
            }),
            "isBase64Encoded": False,
        }

    # Validate inputs here
    if not validateId(carehome, resident):
        return {
            'statusCode': 404,
            'headers': {},
            'body': json.dumps({
                'error': 'module not found'
            }),
            "isBase64Encoded": False,
        }

    new_status = True if new_status == "true" else False

    keys = generateKey(carehome, resident)
    attributes = generateAttributes(name=new_name, status=new_status, wearableId=new_wearable)

    response = table.update_item(Key=keys, AttributeUpdates=attributes)

    return {
        'statusCode': 201,
        'headers': {},
        'body': json.dumps({
            'database-status': response["ResponseMetadata"]["HTTPStatusCode"]
        }),
        "isBase64Encoded": False,
    }


def validateId(carehome, residentId):
    response = table.query(
        KeyConditionExpression=Key('carehome').eq(carehome) & Key('id').eq(residentId)
    )

    return len(response["Items"]) > 0
