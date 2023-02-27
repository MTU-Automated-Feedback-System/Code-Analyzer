import boto3, os

queue_url = os.environ.get('SQS_SUBMISSION')
sqs = boto3.resource('sqs')

def receive_from_queue():
    response = sqs.receive_message(
    QueueUrl=queue_url,
    AttributeNames=[
        'SentTimestamp'
    ],
    MaxNumberOfMessages=1,
    MessageAttributeNames=[
        'All'
    ],
    WaitTimeSeconds=20
    )
    
 