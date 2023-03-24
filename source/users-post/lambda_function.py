import json, boto3
from boto3.dynamodb.conditions import Key
from hashlib import sha256
from secrets import token_hex

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('users')
carehomes = dynamodb.Table('carehomes')


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

    if not isinstance(carehome, str):
        carehome = str(carehome)

    try:
        body = event["body"]
        if isinstance(body, str):
            body = json.loads(body)

        username = body["username"]
        password = body["password"]
        code = body["code"]
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
    role = validateCode(carehome, code)
    if not role:
        return {
            'statusCode': 400,
            'headers': {},
            'body': json.dumps({
                'error': f'invalid carehome/role code'
            }),
            "isBase64Encoded": False,
        }

    if len(username) < 5:
        return {
            'statusCode': 400,
            'headers': {},
            'body': json.dumps({
                'error': f'new username is too short (minimum 5 characters)'
            }),
            "isBase64Encoded": False,
        }

    if len(password) < 8:
        return {
            'statusCode': 400,
            'headers': {},
            'body': json.dumps({
                'error': f'password is too short (minimum 8 characters)'
            }),
            "isBase64Encoded": False,
        }

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


def validateCode(carehome, code):
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
