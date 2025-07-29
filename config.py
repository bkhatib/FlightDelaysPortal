import os
import streamlit as st
from dotenv import load_dotenv

# Load environment variables (for local development)
load_dotenv()

# AWS Credentials (from Streamlit secrets or environment variables)
def get_aws_credentials():
    """Get AWS credentials from Streamlit secrets or environment variables"""
    try:
        # Try Streamlit secrets first (for production)
        if hasattr(st, 'secrets') and st.secrets:
            return {
                'AWS_ACCESS_KEY_ID': st.secrets.get('AWS_ACCESS_KEY_ID'),
                'AWS_SECRET_ACCESS_KEY': st.secrets.get('AWS_SECRET_ACCESS_KEY'),
                'AWS_SESSION_TOKEN': st.secrets.get('AWS_SESSION_TOKEN'),
                'AWS_DEFAULT_REGION': st.secrets.get('AWS_DEFAULT_REGION', 'eu-west-1')
            }
    except:
        pass
    
    # Fallback to environment variables (for local development)
    return {
        'AWS_ACCESS_KEY_ID': os.getenv('AWS_ACCESS_KEY_ID'),
        'AWS_SECRET_ACCESS_KEY': os.getenv('AWS_SECRET_ACCESS_KEY'),
        'AWS_SESSION_TOKEN': os.getenv('AWS_SESSION_TOKEN'),
        'AWS_DEFAULT_REGION': os.getenv('AWS_DEFAULT_REGION', 'eu-west-1')
    }

# Get credentials
credentials = get_aws_credentials()
AWS_ACCESS_KEY_ID = credentials['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = credentials['AWS_SECRET_ACCESS_KEY']
AWS_SESSION_TOKEN = credentials['AWS_SESSION_TOKEN']

# Athena Configuration
ATHENA_DATABASE = os.getenv('ATHENA_DATABASE', "l1_almosafer")  # Database name
ATHENA_TABLE = os.getenv('ATHENA_TABLE', "fact_flight_delay_scheduler")  # Table name
ATHENA_S3_STAGING_DIR = os.getenv('ATHENA_S3_STAGING_DIR', "s3://aws-athena-query-results-032862061730-eu-west-1/")  # Region-specific S3 bucket
ATHENA_REGION = os.getenv('ATHENA_REGION', "eu-west-1")  # AWS region where l1_almosafer database exists
ATHENA_CATALOG = os.getenv('ATHENA_CATALOG', "awsdatacatalog")  # Data source is awsdatacatalog
ATHENA_SCHEMA = os.getenv('ATHENA_SCHEMA', "l1_almosafer")  # Schema name (same as database)
ATHENA_WORKGROUP = os.getenv('ATHENA_WORKGROUP', "primary")  # Primary workgroup (available via API)

# Default query to fetch all data
DEFAULT_QUERY = f"""
SELECT 
    join_key,
    flight_code,
    origin,
    destination,
    dep_delayed,
    cal_dep_delayed_minutes,
    scheduled_departure_date_time_utc,
    actual_departure_date_utc,
    journey_type,
    order_c,
    selling_price_sum,
    gbv_sum,
    departure_date
FROM {ATHENA_DATABASE}.{ATHENA_TABLE}
LIMIT 1000
""" 