import boto3

client = boto3.client('dynamodb')


def lambda_handler(event, context):
    resource = event["methodArn"]

    try:
        sessionId = event["authorizationToken"]
    except KeyError:
        return generatePolicy("", "Deny", resource)

    # Parse resource URI
    request, endpoint, carehome = parseResource(resource)

    # Get session
    session = getSession(carehome, sessionId)

    # Check session exists
    if "Item" not in session:
        return generatePolicy(session, "Deny", resource)

    # Check user is member of the carehome
    if session["Item"]["carehome"]["S"] != carehome:
        return generatePolicy(session, "Deny", resource)

    # Check Permissions
    if session["Item"]["role"]["S"] != getRole(request, endpoint) and session["Item"]["role"]["S"] != "admin":
        return generatePolicy(session, "Deny", resource)

    return generatePolicy(sessionId, "Allow", resource)


# arn:aws:execute-api:us-east-1:269037940490:2r426oxcbj/*/{request}/{endpoint}/{carehome}/{specific}
def parseResource(resource):
    temp = resource.split("/")[2:]

    request = temp[0]
    endpoint = temp[1]
    carehome = temp[2]
    extra = "-extra" if len(temp) == 4 and temp[3] != "" else ""

    endpoint = endpoint + extra

    return request, endpoint, carehome


def getSession(carehome, sessionId):
    return client.get_item(
        TableName='sessions',
        Key={
            'carehome': {'S': carehome},
            'id': {'S': sessionId}
        }
    )


def getRole(request, endpoint):
    response = client.get_item(
        TableName='endpoints',
        Key={
            'endpoint': {'S': endpoint},
            'method': {'S': request},
        }
    )

    if "Item" in response:
        return response["Item"]["role"]["S"]

    # Should never happen but just in case
    return "invalid endpoint"


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
