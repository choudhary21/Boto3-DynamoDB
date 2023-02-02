x = {'Records': 
[
    {'messageId': '35adc39f-b47a-406d-ac0e-0b7f89c83fb9', 
    'receiptHandle': 'AQEBK6vqH/7kz/Ls4Vf/snUS9O1hqa5od/QB25OYR3tMn/GwHBv3luMW16Dywyp8AHUdqcTJgTWEpF/zf+WSBB0e4w7pcWGMMt85NzmYdD2286Rn174gejjCTczm0NkJb3cLdVVuxlrakGvRsknuendvmjQbtmNeOS3cUyh1K1pJUbVbC5e5hOkLUSKLf+OsV50NwBGcXjtiV2azru9ufBpOndAfIUOi8CU5SMRWnGFBkitSycJZTEIx7TH2jhYPDclFX0+6q5mgtRwN5Xlhuk7yRBE+ZsYqc/qzbg5Q0nLbxyquwoyyZr6qVYkdsglflaILq12u/vXhX8fdxJddj/NievoFz+p68DTzj3BPEj5wLPSIE8PcgU+3QpCqn1x74s3K', 
    'body': 'Music', 
    'attributes': {'ApproximateReceiveCount': '20', 'SentTimestamp': '1675145126274', 'SenderId': 'AIDAULWWQD62AL5X6TWXQ', 'ApproximateFirstReceiveTimestamp': '1675145126274'}, 
    'messageAttributes': {}, 
    'md5OfBody': '47dcbd834e669233d7eb8a51456ed217', 
    'eventSource': 'aws:sqs', 
    'eventSourceARN': 'arn:aws:sqs:us-east-1:300023816116:test', 
    'awsRegion': 'us-east-1'}
    ]
    }

print("x: ", x['Records'][0]['body'])