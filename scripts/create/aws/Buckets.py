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
        publicAccessConfiguration={
            'BlockPublicAcls': False,
            'IgnorePublicAcls': False,
            'BlockPublicPolicy': False,
            'RestrictPublicBuckets': False
        }
        region = 'us-west-2'
        location = {'LocationConstraint': region}
        acl_permition = 'public-read'
        cors_rules = {
            'CORSRules': [
            {
                "AllowedHeaders": [
                    "*"
                ],
                "AllowedMethods": [
                    "PUT",
                    "POST",
                    "DELETE",
                    "GET"
                ],
                "AllowedOrigins": [
                    "https://localhost:8080",
                    "http://:192.168.68.107:5173/",
                    "https://soporteinbropi.com/",
                    "https://soporteinbropi.com/"
                ],
                "ExposeHeaders": []
            },
            {
                "AllowedHeaders": [
                    "*"
                ],
                "AllowedMethods": [
                    "PUT",
                    "POST",
                    "DELETE"
                ],
                "AllowedOrigins": [
                    "http://www.example2.com",
                    "http://:192.168.68.107:5173/",
                    "https://soporteinbropi.com/",
                    "https://soporteinbropi.com/"
                ],
                "ExposeHeaders": []
            },
            {
                "AllowedHeaders": [],
                "AllowedMethods": [
                    "GET"
                ],
                "AllowedOrigins": [
                    "*"
                ],
                "ExposeHeaders": []
            }
        ],
        }
        rules = {
            'Rules':[
                {
                    'ObjectOwnership':'ObjectWriter'
                }
            ]
        }
        s3_client.create_bucket( Bucket=nameBucket,
                                CreateBucketConfiguration=location
                            )
        s3_client.put_bucket_ownership_controls(Bucket=nameBucket,
                                                OwnershipControls=rules)
        s3_client.put_public_access_block(Bucket=nameBucket,
                                          PublicAccessBlockConfiguration=publicAccessConfiguration)
        s3_client.put_bucket_acl(Bucket=nameBucket,
                                 ACL=acl_permition)
        
        s3_client.put_bucket_cors(Bucket=nameBucket,
                                  CORSConfiguration=cors_rules)
    except Exception as e:
        logging.error(e)
        raise False

async  def add_policytu(nameBucket):
    try:
        s3 = createClient()
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
        s3.put_bucket_policy(Bucket=nameBucket, Policy=bucket_policy) 
       
    except Exception as e:
        logging.error('add_policytu',e)
        raise False
   

async def create(nameBucket):
    await create_buckets(nameBucket)
    await add_policytu(nameBucket)
    return True