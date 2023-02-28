"""
    Commenting everything out here as this is more of an example and information learned during research
    Those are still possible options
"""

# import boto3, os
# from kombu.utils.url import safequote


# # option using celery sqs
# queue_url = os.environ.get('SQS_SUBMISSION')
# access_key = safequote(os.environ.get('ACCESS_KEY'))
# secret_key = safequote(os.environ.get('SECRET_KEY'))

# broker_url = f"sqs://{access_key}:{secret_key}@"
# broker_transport_options = {
#     'region': 'eu-west-1',
#     'visibility_timeout': 600,
#     'wait_time_seconds': 20,
#     'predefined_queues': {
#         'SubmissionQueue': {
#             'url': queue_url,
#             'access_key_id': access_key,
#             'secret_access_key': secret_key,
#         }
#     }
# } 

# # optino polling data from sqs using boto3
# sqs = boto3.resource('sqs')

# def receive_from_queue():
#     response = sqs.receive_message(
#     QueueUrl=queue_url,
#     AttributeNames=[
#         'SentTimestamp'
#     ],
#     MaxNumberOfMessages=1,
#     MessageAttributeNames=[
#         'All'
#     ],
#     WaitTimeSeconds=20
#     )
    
 