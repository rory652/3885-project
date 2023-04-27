import json, boto3
from boto3.dynamodb.conditions import Key
from secrets import token_hex
from hashlib import sha256

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('carehomes')


def generateItem(carehome, nurse, admin):
    return {
        'id': carehome,
        'nurse-code': nurse,
        'admin-code': admin
    }


def lambda_handler(event, context):
    carehome = generateId()

    nurseCode, nurseHash = generateCode()
    adminCode, adminHash = generateCode()

    response = table.put_item(Item=generateItem(carehome, nurseHash, adminHash))

    return {
        'statusCode': 201,
        'headers': {
            "carehome": carehome,
            "nurse-code": nurseCode,
            "admin-code": adminCode,
            "Access-Control-Allow-Origin": "*"
        },
        'body': json.dumps({
            'database-status': response["ResponseMetadata"]["HTTPStatusCode"]
        }),
        "isBase64Encoded": False,
    }


def generateId():
    valid = False
    generated = token_hex(8)

    while not valid:
        response = table.query(
            KeyConditionExpression=Key('id').eq(generated)
        )

        if len(response["Items"]) == 0:
            valid = True
        else:
            generated = token_hex(8)

    return generated


def generateCode():
    generated = token_hex(8)
    hashed = sha256(generated.encode()).hexdigest()

    return generated, hashed
