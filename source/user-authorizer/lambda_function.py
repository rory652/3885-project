import boto3

client = boto3.client('dynamodb')


def lambda_handler(event, context):
    resource = event["methodArn"]

    try:
        sessionId = event["authorizationToken"]
    except KeyError:
        return generatePolicy("", "Deny", resource)

    # Parse resource URI
    carehome, endpoint, username = parseResource(resource)

    print(carehome, endpoint, username)

    # Get session
    session = getSession(carehome, sessionId)

    # Check session exists
    if "Item" not in session:
        return generatePolicy(session, "Deny", resource)

    # Check user is member of the carehome
    if session["Item"]["carehome"]["S"] != carehome:
        return generatePolicy(session, "Deny", resource)

    # Check Permissions
    if session["Item"]["username"]["S"] != username and endpoint != "login":
        return generatePolicy(session, "Deny", resource)

    return generatePolicy(sessionId, "Allow", resource)


# arn:aws:execute-api:us-east-1:269037940490:2r426oxcbj/*/{request}/{carehome}/{endpoint}/{username}
def parseResource(resource):
    temp = resource.split("/")[2:]

    try:
        carehome = temp[1]
        endpoint = temp[2]
        username = temp[3]
    except:
        username = ""

    print(temp)

    return carehome, endpoint, username


def getSession(carehome, sessionId):
    return client.get_item(
        TableName='sessions',
        Key={
            'carehome': {'S': carehome},
            'id': {'S': sessionId}
        }
    )


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
