import boto3
import time
import pandas as pd
import os

test_csv_file_path = os.path.join('read_from_s3', 'test', 'utils', 'files', 'class.csv')
mean_value = (10 + 8 + 7)/3

def mount_csv(data):
    rows = [','.join(list(data.columns))]
    for row in data.values:
        rows.append(','.join(map(str, row)))
    rows = '\n'.join(rows)
    return rows

def test_localstack():
    config_s3 = {
        'service_name': 's3',
        'aws_access_key_id': '123',
        'aws_secret_access_key': '123',
        'endpoint_url': 'http://localhost:4566'
    }

    bucket = 'muly-dev'
    input_key = 'uploads/class.csv'
    output_key = 'output/final_data.csv'

    test_file = mount_csv(pd.read_csv(test_csv_file_path))
    client = boto3.client(**config_s3)
    client.put_object(Body=test_file, Bucket=bucket, Key=input_key, ContentType='csv')

    n_files = 0
    initial_time = time.time()
    while ((n_files == 0) and ((time.time() - initial_time) < 50)):
        objects_list = client.list_objects_v2(Bucket=bucket, Prefix='output')
        n_files = objects_list['KeyCount']

    obj = client.get_object(Bucket=bucket, Key=output_key)['Body']
    res = pd.read_csv(obj).to_dict()
    correct_res = {'NAME': {0: 'a', 1: 'b', 2: 'c', 3: 'MEAN'}, 'POINTS': {0: 10, 1: 8, 2: 7, 3: mean_value}}
    assert res == correct_res