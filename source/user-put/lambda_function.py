import json, boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('users')


def generateKey(carehome, username):
    return {
        'carehome': carehome,
        'username': username,
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

    username = event["pathParameters"]["username"]

    try:
        body = event["body"]
        if isinstance(body, str):
            body = json.loads(body)

        new_username = body["new_username"]
        # new_password = body["new_password"] - hash later
        new_role = body["new_role"]
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
    if not validateId(carehome, username):
        return {
            'statusCode': 404,
            'headers': {},
            'body': json.dumps({
                'error': 'module not found'
            }),
            "isBase64Encoded": False,
        }

    keys = generateKey(carehome, username)
    attributes = generateAttributes(username=new_username, role=new_role)

    response = table.update_item(Key=keys, AttributeUpdates=attributes)

    return {
        'statusCode': 201,
        'headers': {},
        'body': json.dumps({
            'database-status': response["ResponseMetadata"]["HTTPStatusCode"]
        }),
        "isBase64Encoded": False,
    }


def validateId(carehome, username):
    response = table.query(
        KeyConditionExpression=Key('carehome').eq(carehome) & Key('username').eq(username)
    )

    return len(response["Items"]) > 0
