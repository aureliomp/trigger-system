import boto3
import config as systemC
from botocore.client import  Config
import logging
import json

config =  Config(
    signature_version = 's3v4'
) 


def createClient():
    app_config  = systemC.load_info()
    s3_client = boto3.client('s3',
                aws_access_key_id = app_config['aws']['id'] ,
                aws_secret_access_key = app_config['aws']['key'] , 
                config=config
    )
    return s3_client

async def create_buckets(nameBucket):
    try:
        s3_client = createClient()
        # s3_client.create_bucket(Bucket=nameBucket)
        region = 'us-west-2'
        location = {'LocationConstraint': region}
        s3_client.create_bucket(Bucket=nameBucket,
                                    CreateBucketConfiguration=location)
        print('se creo la cubeta')
    except Exception as e:
        logging.error(e)
        raise False

async  def add_policytu(nameBucket):
    try:
        s3 = createClient()
        #ctm-python
        #{"Version":"2012-10-17","Statement":[{"Sid":"PublicRead","Effect":"Allow","Principal":"*","Action":["s3:GetObject","s3:GetObjectVersion"],"Resource":"arn:aws:s3:::ctm-script/*"}]}

        bucket_policy = {
            'Version':'2012-10-17',
            'Statement':[
                {
                    'Sid':'PublicRead',
                    'Effect':'Allow',
                    'Principal':'*',
                    'Action':[
                        's3:GetObject',
                        's3:GetObjectVersion'
                    ],
                    'Resource':f'arn:aws:s3:::{nameBucket}/*'
                }]
            }
        bucket_policy = json.dumps(bucket_policy)
        print('bucket_policy',bucket_policy)
        s3.put_bucket_policy(Bucket=nameBucket, Policy=bucket_policy)
    except Exception as e:
        logging.error('add_policytu',e)
        raise False
   

async def create(nameBucket):
    # await create_buckets(nameBucket)
    await add_policytu(nameBucket)
    """ 
        response = s3_client.list_buckets()
        for bucket in response['Buckets']:
            print(bucket['Name']) 
        
    """
    
    # print('se creo una cubeta',nameBucket)
    # hello_s3()
    return True