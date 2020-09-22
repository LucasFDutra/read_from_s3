from read_from_s3.src import handler
import pandas as pd
from read_from_s3.test.utils.mock import Client
import json
import os

test_csv_file_path = os.path.join('read_from_s3', 'test', 'utils', 'files', 'class.csv')
test_event_file_path = os.path.join('read_from_s3', 'test', 'utils', 'files', 'event.json')
mean_value = (10 + 8 + 7)/3

def test_read_csv():
    data = handler.read_csv(test_csv_file_path).to_dict()
    correct_res = {'NAME': {0: 'a', 1: 'b', 2: 'c'}, 'POINTS': {0: 10, 1: 8, 2: 7}}
    assert data == correct_res

def test_get_mean():
    test_data = pd.read_csv(test_csv_file_path)
    assert handler.get_mean(test_data) == mean_value

def test_add_mean_to_data_frame():
    test_data = pd.read_csv(test_csv_file_path)
    res = handler.add_mean_to_data_frame(test_data, mean_value).to_dict()
    correct_res = {'NAME': {0: 'a', 1: 'b', 2: 'c', 3: 'MEAN'}, 'POINTS': {0: 10, 1: 8, 2: 7, 3: mean_value}}
    assert res == correct_res

def test_save_in_s3():
    client = Client.Client()
    data = pd.DataFrame({'NAME': {0: 'a', 1: 'b', 2: 'c', 3: 'MEAN'}, 'POINTS': {0: 10, 1: 8, 2: 7, 3: mean_value}})
    assert handler.save_in_s3(data, client, 'muly-dev') == True

def test_get_client_local():
    os.environ['LOCALSTACK_HOSTNAME'] = 'localhost'
    correct_res = {
        'service_name': 's3',
        'aws_access_key_id': '123',
        'aws_secret_access_key': '123',
        'endpoint_url': 'http://localhost:4566'
    }
    res = handler.get_client()
    assert res == correct_res

def test_get_client_cloud():
    del os.environ['LOCALSTACK_HOSTNAME']
    correct_res = {
        'service_name': 's3'
    }
    res = handler.get_client()
    assert res == correct_res

def test_main():
    client = Client.Client()
    with open(test_event_file_path, 'r') as event_file:
        event = json.load(event_file)
    assert handler.main(event, client) == True

