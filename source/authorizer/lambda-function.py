import boto3

client = boto3.client('dynamodb')


def lambda_handler(event, context):
    resource = event["methodArn"]

    try:
        sessionId = event["authorizationToken"]
    except KeyError:
        return generatePolicy("", "Deny", resource)

    # Get session
    session = getSession(sessionId)

    # Parse resource URI
    request, endpoint, carehome, extra = parseResource(resource)

    # Check session exists
    if "Item" not in session:
        return generatePolicy(session, "Deny", resource)

    # Check user is member of the carehome
    if session["Item"]["carehome"]["S"] != carehome:
        return generatePolicy(session, "Deny", resource)

    # Check Permissions
    if session["Item"]["role"]["S"] != getRole(request, endpoint, extra):
        return generatePolicy(session, "Deny", resource)

    return generatePolicy(sessionId, "Allow", resource)


# arn:aws:execute-api:us-east-1:269037940490:2r426oxcbj/*/{request}/{endpoint}/{carehome}/{specific}
def parseResource(resource):
    temp = resource.split("/")[2:]

    request = temp[0]
    endpoint = temp[1]
    carehome = temp[2]
    extra = True if len(temp) == 4 and temp[3] != "" else False

    return request, endpoint, carehome, extra


def getSession(sessionId):
    return client.get_item(
        TableName='sessions',
        Key={
            'id': {'S': sessionId}
        }
    )


def getRole(request, endpoint, extra):
    return "nurse"


def generatePolicy(sessionId, effect, resource):
    return {
        "principalId": sessionId,
        "policyDocument": {
            "Version": "2012-10-17",
            "Statement": {
                "Action": "execute-api:invoke",
                "Effect": effect,
                "Resource": resource,
            }
        }
    }
