import json, boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('residents')

standardHeaders = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Request-Headers": "SESSION-ID"
}


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
    carehome = event["pathParameters"]["carehome-id"]

    if not isinstance(carehome, str):
        carehome = str(carehome)

    resident = event["pathParameters"]["resident-id"]

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
            'headers': {
                "Access-Control-Allow-Origin": "*"
            },
            'body': json.dumps({
                'error': f'{str(err)} field missing - set to empty string to not update'
            }),
            "isBase64Encoded": False,
        }

    # Validate inputs here
    if not validateId(carehome, resident):
        return {
            'statusCode': 404,
            'headers': {
                "Access-Control-Allow-Origin": "*"
            },
            'body': json.dumps({
                'error': 'module not found'
            }),
            "isBase64Encoded": False,
        }

    keys = generateKey(carehome, resident)
    attributes = generateAttributes(name=new_name, status=new_status, wearableId=new_wearable)

    response = table.update_item(Key=keys, AttributeUpdates=attributes)

    return {
        'statusCode': 201,
        'headers': standardHeaders,
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
