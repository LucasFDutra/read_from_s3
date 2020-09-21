import boto3
import json

config_cw_logs = {
    'service_name': 'logs',
    'aws_access_key_id': '123',
    'aws_secret_access_key': '123',
    'region_name': 'us-east-1',
    'endpoint_url': 'http://localhost:4566'
}

cw_logs = boto3.client(**config_cw_logs)

logGroupName = cw_logs.describe_log_groups()['logGroups'][0]['logGroupName']

logStreams = cw_logs.describe_log_streams(logGroupName=logGroupName)['logStreams']

logs_msg = []
for logStream in logStreams:
    logStreamName = logStream['logStreamName']
    logs = cw_logs.get_log_events(logGroupName=logGroupName, logStreamName=logStreamName)
    for log in logs['events']:
        print('------------------------------------------------------------------')
        print(log['message'])