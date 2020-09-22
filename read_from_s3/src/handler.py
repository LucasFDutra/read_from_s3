import json
import boto3
import os
import pandas as pd

def get_client():
    if ('LOCALSTACK_HOSTNAME' in os.environ):
        client_config = {
            'service_name': 's3',
            'aws_access_key_id': '123',
            'aws_secret_access_key': '123',
            'endpoint_url': 'http://'+os.environ['LOCALSTACK_HOSTNAME']+':4566'
        }
    else:
        client_config = {
            'service_name': 's3'
        }
    return client_config

def save_in_s3(data, client, bucket):
    rows = [','.join(list(data.columns))]
    for row in data.values:
        rows.append(','.join(map(str, row)))
    rows = '\n'.join(rows)
    file_name = 'output/final_data.csv'
    client.put_object(Body=rows, Bucket=bucket, Key=file_name, ContentType='csv') 
    print('Arquivo '+ file_name +' subiu com sucesso')
    return True

def add_mean_to_data_frame(data, mean):
    new_line = pd.DataFrame([['MEAN', mean]], columns=['NAME', 'POINTS'])
    new_data = pd.concat([data, new_line]).reset_index(drop=True)
    return new_data

def get_mean(data):
    return data.POINTS.mean()

def read_csv(file_path):
    data = pd.read_csv(file_path)
    print(data)
    return data

def main(event, client):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    obj = client.get_object(Bucket=bucket, Key=key)['Body']
    data = read_csv(obj)
    mean = get_mean(data)
    data = add_mean_to_data_frame(data, mean)
    return save_in_s3(data, client, bucket)

def lambda_handler(event, context):
    client_config = get_client()
    client = boto3.client(**client_config)
    return main(event, client)