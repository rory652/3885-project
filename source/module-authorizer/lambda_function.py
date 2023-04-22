import boto3
from boto3.dynamodb.conditions import Key
from hashlib import sha256

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('modules')


def lambda_handler(event, context):
    resource = event["methodArn"]
    try:
        carehome = resource.split("/")[3]
    except IndexError:
        carehome = "testing"

    try:
        moduleId = event["authorizationToken"]
    except KeyError:
        return generatePolicy("", "Deny", resource)

    moduleHash = sha256(moduleId.encode()).hexdigest()

    if checkHash(carehome, moduleHash):
        return generatePolicy(moduleId, "Allow", resource)

    return generatePolicy(moduleId, "Deny", resource)


def checkHash(carehome, module):
    response = table.query(
        KeyConditionExpression=Key('carehome').eq(carehome) & Key('id').eq(module)
    )

    return response["Items"]


def generatePolicy(moduleId, effect, resource):
    return {
        "principalId": moduleId,
        "policyDocument": {
            "Version": "2012-10-17",
            "Statement": {
                "Action": "execute-api:invoke",
                "Effect": effect,
                "Resource": resource,
            }
        }
    }
