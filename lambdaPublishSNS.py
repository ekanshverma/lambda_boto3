#### lambda function will publish SNS message when an Event occurs on RDS ########
import boto3
import json
sns = boto3.client('sns')
def handler(event,context):
    input_event=event
    parsed = eval(input_event['Records'][0]['body'])
    search_str=eval(parsed['Message'])['Event Message']
    parsed_str=str(parsed)
    conditions=["fail","failure","start","recovery","shutdown"]
    for x in conditions:
        if search_str.find(x)!=-1:
            response = sns.publish(
                TopicArn='=========== ARN of SNS Topic ================',    
                Message=parsed_str
            )
