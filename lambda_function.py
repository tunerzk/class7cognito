import json

def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'headers': {
            "Content-Type": "application/json"
        },
        'body': json.dumps({
            "message": "Hello from Lambda!",
            "user": event.get("requestContext", {})
                        .get("authorizer", {})
                        .get("principalId", "unknown")
        })
    }
