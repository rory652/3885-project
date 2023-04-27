import json, boto3
from boto3.dynamodb.conditions import Key
from hashlib import sha256

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('users')
carehomes = dynamodb.Table('carehomes')


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
    carehome = event["pathParameters"]["carehome-id"]

    if not isinstance(carehome, str):
        carehome = str(carehome)

    username = event["pathParameters"]["username"]

    try:
        body = event["body"]
        if isinstance(body, str):
            body = json.loads(body)

        new_username = body["new_username"]
        # new_password = body["new_password"] - hash later
        new_code = body["new_code"]
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
    if len(new_username) < 5 and new_username != "":
        return {
            'statusCode': 400,
            'headers': {
                "Access-Control-Allow-Origin": "*"
            },
            'body': json.dumps({
                'error': f'new username is too short (minimum 5 characters)'
            }),
            "isBase64Encoded": False,
        }

    if not validateUser(carehome, username):
        return {
            'statusCode': 404,
            'headers': {
                "Access-Control-Allow-Origin": "*"
            },
            'body': json.dumps({
                'error': 'user not found'
            }),
            "isBase64Encoded": False,
        }

    if (new_role := validateCode(carehome, new_code)) == False:
        return {
            'statusCode': 404,
            'headers': {
                "Access-Control-Allow-Origin": "*"
            },
            'body': json.dumps({
                'error': 'user not found'
            }),
            "isBase64Encoded": False,
        }

    keys = generateKey(carehome, username)
    attributes = generateAttributes(username=new_username, role=new_role)

    response = table.update_item(Key=keys, AttributeUpdates=attributes)

    return {
        'statusCode': 201,
        'headers': {
            "Access-Control-Allow-Origin": "*"
        },
        'body': json.dumps({
            'database-status': response["ResponseMetadata"]["HTTPStatusCode"]
        }),
        "isBase64Encoded": False,
    }


def validateCode(carehome, code):
    if code == "":
        return ""

    response = carehomes.query(
        KeyConditionExpression=Key('id').eq(carehome)
    )

    if not response["Items"]:
        return False

    hashed = sha256(code.encode()).hexdigest()

    if hashed == response["Items"][0]["nurse-code"]:
        return "nurse"
    elif hashed == response["Items"][0]["admin-code"]:
        return "admin"
    else:
        return False


def validateUser(carehome, username):
    response = table.query(
        KeyConditionExpression=Key('carehome').eq(carehome) & Key('username').eq(username)
    )

    return len(response["Items"]) > 0
