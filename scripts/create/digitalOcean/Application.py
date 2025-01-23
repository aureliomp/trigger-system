import config 
from pydo import Client
import json
import yaml


async def  create(req):
    config_data = config.load_info()
    client = Client(token=config_data['digitalOcean']['key'])
    # response = client.apps.list()


    with open('./dataBook/digitalOcean.yaml','r') as f:
        yamlData = yaml.safe_load(f)
        if  yamlData['name'] == 'my-app':
            yamlData['name'] = req.nameApplication
        for env in yamlData['services'][0]['envs']:
            if env['key'] == 'MYSQL_DATABASE':
               env['value'] = req.name
    print(yamlData)
    # print('data',config_data['digitalOcean']['key'])