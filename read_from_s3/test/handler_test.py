from read_from_s3.src import handler
import pandas as pd
from read_from_s3.test.mock import Client
import json


def test_read_csv():
    data = handler.read_csv('read_from_s3/test/files/class.csv').to_dict()
    correct_res = {'NAME': {0: 'Lucas', 1: 'Felipe', 2: 'Carlos'}, 'POINTS': {0: 10, 1: 8, 2: 7}}
    assert data == correct_res

def test_get_mean():
    test_data = pd.read_csv('read_from_s3/test/files/class.csv')
    correct_res = (10 + 8 + 7)/3
    assert handler.get_mean(test_data) == correct_res

def test_add_mean_to_data_frame():
    test_data = pd.read_csv('read_from_s3/test/files/class.csv')
    mean = (10 + 8 + 7)/3
    res = handler.add_mean_to_data_frame(test_data, mean).to_dict()
    correct_res = {'NAME': {0: 'Lucas', 1: 'Felipe', 2: 'Carlos', 3: 'MEAN'}, 'POINTS': {0: 10, 1: 8, 2: 7, 3: mean}}
    assert res == correct_res

def test_save_in_s3():
    client = Client.Client()
    mean = (10 + 8 + 7)/3
    data = pd.DataFrame({'NAME': {0: 'Lucas', 1: 'Felipe', 2: 'Carlos', 3: 'MEAN'}, 'POINTS': {0: 10, 1: 8, 2: 7, 3: mean}})
    assert handler.save_in_s3(data, client, 'muly-dev') == True

def test_main():
    client = Client.Client()
    mean = (10 + 8 + 7)/3
    with open('read_from_s3/test/files/event.json', 'r') as event_file:
        event = json.load(event_file)
    assert handler.main(event, client) == True