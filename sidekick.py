import logging
import os
import pathlib
import json
import requests

logging.basicConfig(level=logging.INFO)

config = {}
cwd = pathlib.Path(__file__).parent.resolve()
path = str(cwd) + '/config.json'
with open(path) as f:
    config = json.load(f)

headers = {'Authorization': f'Bearer {config["TOKEN"]}'}
response = requests.get('https://api.binarylane.com.au/v2/data_usages/current', headers=headers)
json = response.json()

transfer_gigabytes_total = 0
current_transfer_usage_gigabytes_total = 0
for data_usage in json['data_usages']:
    current_transfer_usage_gigabytes_total += data_usage['current_transfer_usage_gigabytes']
    transfer_gigabytes_total += data_usage['transfer_gigabytes']
logging.info(f'{current_transfer_usage_gigabytes_total}/{transfer_gigabytes_total}G used')

state = 'enable'
if (current_transfer_usage_gigabytes_total > transfer_gigabytes_total * 0.8):
    state = 'disable'

os.system(f'mcli admin user {state} local {config["USER"]}')
logging.info(f'{config["USER"]} {state}d')
