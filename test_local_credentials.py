#!/usr/bin/env python3

import os
import boto3
from config import *

def test_credentials():
    print("Testing AWS Credentials...")
    print(f"AWS_ACCESS_KEY_ID: {AWS_ACCESS_KEY_ID[:10] if AWS_ACCESS_KEY_ID else 'None'}...")
    print(f"AWS_SECRET_ACCESS_KEY: {AWS_SECRET_ACCESS_KEY[:10] if AWS_SECRET_ACCESS_KEY else 'None'}...")
    print(f"AWS_SESSION_TOKEN: {AWS_SESSION_TOKEN[:10] if AWS_SESSION_TOKEN else 'None'}...")
    print(f"ATHENA_REGION: {ATHENA_REGION}")
    print(f"ATHENA_DATABASE: {ATHENA_DATABASE}")
    
    try:
        # Test boto3 session
        session = boto3.Session(
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            aws_session_token=AWS_SESSION_TOKEN,
            region_name=ATHENA_REGION
        )
        
        # Test Athena client
        athena_client = session.client('athena')
        print("✅ Successfully created Athena client!")
        
        # Test a simple query
        query = f"SELECT COUNT(*) as count FROM {ATHENA_DATABASE}.{ATHENA_TABLE} LIMIT 1"
        print(f"Testing query: {query}")
        
        response = athena_client.start_query_execution(
            QueryString=query,
            QueryExecutionContext={
                'Database': ATHENA_DATABASE,
                'Catalog': ATHENA_CATALOG
            },
            ResultConfiguration={
                'OutputLocation': ATHENA_S3_STAGING_DIR
            },
            WorkGroup=ATHENA_WORKGROUP
        )
        
        print(f"✅ Query started successfully! Query ID: {response['QueryExecutionId']}")
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    test_credentials() 