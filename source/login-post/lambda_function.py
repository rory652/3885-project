import json, boto3
from boto3.dynamodb.conditions import Key
from hashlib import sha256
from secrets import token_hex

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('sessions')
users = dynamodb.Table('users')


def generateItem(carehome, session, username, role):
    return {
        'carehome': carehome,
        'id': session,
        'username': username,
        'role': role,
    }


def generateResponse(status, body, headers=None):
    if headers is None:
        headers = {}
    return {
        'statusCode': status,
        'headers': headers,
        'body': json.dumps(body),
        "isBase64Encoded": False,
    }


def lambda_handler(event, context):
    carehome = event["pathParameters"]["carehome-id"]

    if not isinstance(carehome, str):
        carehome = str(carehome)

    try:
        body = event["body"]
        if isinstance(body, str):
            body = json.loads(body)

        username = body["username"]
        password = body["password"]
    except KeyError as err:
        return generateResponse(400, {'error': f'{str(err)} field missing'})

    user = getUser(carehome, username)

    # Validate inputs here
    if len(user) == 0:
        return generateResponse(400, {'error': 'user not found'})

    if checkSession(carehome, username):
        return generateResponse(400, {'error': 'user already logged in'})

    if hashPassword(password, user[0]["salt"]) != user[0]["password"]:
        return generateResponse(400, {'error': 'incorrect password'})

    sessionId = generateSession(carehome)
    response = table.put_item(Item=generateItem(carehome, sessionId, username, user[0]["role"]))

    return generateResponse(200, {'database-status': response["ResponseMetadata"]["HTTPStatusCode"]},
                            headers={
                                "SESSION-ID": sessionId,
                                "Access-Control-Allow-Origin": "*",
                                "Access-Control-Expose-Headers": "SESSION-ID"
                            })


def getUser(carehome, username):
    response = users.query(
        KeyConditionExpression=Key('carehome').eq(carehome) & Key('username').eq(username)
    )

    return response["Items"]


def checkSession(carehome, username):
    response = table.query(
        KeyConditionExpression=Key('carehome').eq(carehome)
    )

    for session in response["Items"]:
        if session["username"] == username:
            return True

    return False


def generateSession(carehome):
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


def hashPassword(password, salt):
    h = sha256("".join([password, salt]).encode()).digest()
    # Repeatedly hash - slow down algorithm
    for i in range(100):
        h = sha256(h).digest()

    return sha256(h).hexdigest()
