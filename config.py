import os
# importing necessary functions from dotenv library
from dotenv import dotenv_values

def load_info():
    config = dotenv_values(".env")
    mysql = dict(
        host= config['HOST'],
        user= config['USER'],
        port= config['PORT'],
        password= config['PASSWORD']
    )
    return  mysql

# print(os.getenv)
# https://www.youtube.com/shorts/12eTCTns_B4