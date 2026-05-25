Phase 1 — Create DynamoDB Table

Navigation
    DynamoDB
    Create Table

    Table Name: token-tracking
    Partition Key: token_id
    Type:: String
    Capacity Mode: On-demand

Table Purpose

Each token gets tracked:

    {
      "token_id": "abc123",
      "username": "student1",
      "issued_at": "2026-05-19T20:00:00Z",
      "used": false
    }


Phase 2 — Modify get_token.py

Now the script becomes:

    auth utility
    telemetry producer

Add DynamoDB Write---> After successful authentication:
modify your get_token.py


    import uuid
    from datetime import datetime
    
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("token-tracking")
    
    token_id = str(uuid.uuid4())
    
    table.put_item(
        Item={
            "token_id": token_id,
            "username": username,
            "issued_at": datetime.utcnow().isoformat(),
            "used": False
        }
    )


Phase 3 — Mark Token Used

When Lambda receives valid request: Update DynamoDB:
Update your previous Lambda with this: https://github.com/BalericaAI/lambda/blob/main/lessonf/lambda/update_token.py

If you want to play with headers then.... Pass token_id as header: -H "x-token-id: abc123"

Phase 4 — Create Detection Lambda

Lambda Name: unused-token-detector

Purpose

Find tokens:

        used = false
        AND
        older than 10 minutes


detection.py  Here: https://github.com/BalericaAI/lambda/blob/main/lessonf/lambda/detection.py

Phase 5 — EventBridge Schedule

Navigation
        EventBridge
        Rules
        Create Rule


Name: unused-token-check
Rule Type: Schedule
Schedule: rate(5 minutes
Target: unused-token-detector Lambda

Is this fun? Say "Lizzo Luvs Me" If this is fun for you!!!

Phase 6 — Generate Alert

Initially: CloudWatch log only

Example: ALERT: student1 generated token but never used it
ALERT: student2 paid Keisha rent yet didn't smash

I think this is enough for this week.  Would you like to SOAR above Black IT Network? 



