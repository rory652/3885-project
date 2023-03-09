import json, boto3
from boto3.dynamodb.conditions import Key
from hashlib import sha256
from secrets import token_hex

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('users')


def generateItem(carehome, username, password, role, salt):
    return {
        'carehome': carehome,
        'username': username,
        'password': password,
        'role': role,
        'salt': salt
    }


def lambda_handler(event, context):
    carehome = event["pathParameters"]["carehomeId"]

    if type(carehome) != str:
        carehome = str(carehome)

    try:
        body = event["body"]
        if type(event["body"]) == str:
            body = json.loads(body)

        username = body["username"]
        password = body["password"]
        role = body["role"]
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
    if not validateUsername(carehome, username):
        return {
            'statusCode': 400,
            'headers': {},
            'body': json.dumps({
                'error': f'username taken'
            }),
            "isBase64Encoded": False,
        }

    password, salt = hashPassword(password)

    response = table.put_item(Item=generateItem(carehome, username, password, role, salt))

    return {
        'statusCode': 201,
        'headers': {},
        'body': json.dumps({
            'database-status': response["ResponseMetadata"]["HTTPStatusCode"]
        }),
        "isBase64Encoded": False,
    }


def validateUsername(carehome, username):
    response = table.query(
        KeyConditionExpression=Key('carehome').eq(carehome) & Key('username').eq(username)
    )

    return len(response["Items"]) == 0


def hashPassword(password):
    salt = token_hex(16)

    h = sha256("".join([password, salt]).encode()).digest()
    # Repeatedly hash - slow down algorithm
    for i in range(100):
        h = sha256(h).digest()

    return sha256(h).hexdigest(), salt
