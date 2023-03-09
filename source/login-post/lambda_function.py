import boto3

client = boto3.client('dynamodb')


def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'endpoint': 'login',
        'request': 'POST'
    }