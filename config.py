import os
# importing necessary functions from dotenv library
from dotenv import dotenv_values

def load_info():
    config = dotenv_values(".env")
    mysql = dict(
        host = config['MYSQL_HOST'],
        user = config['MYSQL_USER'],
        port = config['MYSQL_PORT'],
        password = config['MYSQL_PASSWORD']
    )
    aws = dict(
        id = config['AWS_ACCESS_KEY_ID'],
        key = config['AWS_SECRET_ACCESS_KEY' ]
    )
    env_data = dict()
    env_data['mysql'] = mysql
    env_data['aws'] = aws
    return  env_data

# https://www.youtube.com/shorts/12eTCTns_B4