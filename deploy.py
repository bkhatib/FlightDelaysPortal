#!/usr/bin/env python3
"""
Deployment helper script for Flight Delays Portal
This script helps prepare the application for deployment to Streamlit Cloud
"""

import os
import sys
import json
from pathlib import Path

def create_streamlit_config():
    """Create Streamlit configuration file"""
    config_content = """
[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
"""
    
    config_dir = Path(".streamlit")
    config_dir.mkdir(exist_ok=True)
    
    config_file = config_dir / "config.toml"
    with open(config_file, "w") as f:
        f.write(config_content.strip())
    
    print(f"✅ Created Streamlit config at {config_file}")

def create_env_template():
    """Create environment variables template"""
    env_template = """# AWS Configuration
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
AWS_SESSION_TOKEN=your_session_token_here

# Athena Configuration
ATHENA_DATABASE=your_database_name
ATHENA_TABLE=your_table_name
ATHENA_S3_STAGING_DIR=s3://your-bucket/athena-results/
ATHENA_REGION=us-east-1

# Optional: Override config.py settings
# Set these in Streamlit Cloud environment variables
"""
    
    with open(".env.template", "w") as f:
        f.write(env_template.strip())
    
    print("✅ Created .env.template file")

def update_config_for_deployment():
    """Update config.py to use environment variables for deployment"""
    config_content = '''import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# AWS Athena Configuration
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "ASIAQPJV3ISRLZ6XP7OH")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "hgttADotkbRDgkJEPbsD8XYsXrG2MlR10lCH77GN")
AWS_SESSION_TOKEN = os.getenv("AWS_SESSION_TOKEN", "IQoJb3JpZ2luX2VjEGUaCWV1LXdlc3QtMSJGMEQCIBUfg8C9q7EXqfGNqRifGCRqm3NWhW6sAWXdwPG/9NALAiAcoPGTP67E1Osk6MCl5VBhs/wNnZnE7aOjHWmZ8b1phiqUAwiN//////////8BEAIaDDAzMjg2MjA2MTczMCIMdbGzX3ePsx+BAoCeKugCD19/1C9YjbIPTMd7mypztTBIbw9bdIJmdTHYlzqLIbCCflqV+S/ari3KtfUgQ+9aKmPT436J9Q1vbaSE/h74VQuP9yzjZDPsyTqZTEjoEhMh00ChrCcfy+r7mojoznl/Dyf4pYqw2a6MqsHFDV6+vfp37Q0lSvo3gfANXu4xlpMyuOLF6MsvT1ze2Z0YIYGBeWdDnXp86b8QxbyPNSCPUfExL1O0CPvwXLsEoQ30VxzKqXFIVEmKru/zj6oRrqUz/dHXhiQlaM+LHQjazZ/J0lss2xQNJTdH+HxH2nmow/ABpS7MNNmXoQCihI2s+owQIRx34ctS1171F6i4MNxP0ooetmnkgg3Ctxv+i7yMIzQjVnfEJHygTPEt1TD5gVCwADxVASGIFewTvgysjqD+cxJUy/nhAumr3KqGqM1boCGGJ1ac8CbXd2mWz0jF3qf87zsQPsbn6+GkVUFY86k6Tp/3o+yUDlxgMPfSncQGOqcBoGPRgBY+yKdTxU93mSM7+fTcRi7RpTrLV0aTQx9tzTVgCDCskN6BWTZ0i4pYTuFoWiEAiMJiu6m41btZzamNlSz8qgZ1BdFKgLyjQlQzIO0AsQCWjahkiArd2KQGzMPX4d7aTo2dIAz6Z5z/qwedFssJF1IjC1c0ymtFTdKsA24XiX5rIi3XsbXnAlt05Sx+C/N842xXUpfeN0jvnKQbiPUBLSceEgs=")

# Athena Configuration
ATHENA_DATABASE = os.getenv("ATHENA_DATABASE", "your_database_name")
ATHENA_TABLE = os.getenv("ATHENA_TABLE", "your_table_name")
ATHENA_S3_STAGING_DIR = os.getenv("ATHENA_S3_STAGING_DIR", "s3://your-bucket/athena-results/")
ATHENA_REGION = os.getenv("ATHENA_REGION", "us-east-1")

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
'''
    
    with open("config.py", "w") as f:
        f.write(config_content.strip())
    
    print("✅ Updated config.py for deployment")

def create_deployment_guide():
    """Create a deployment guide markdown file"""
    guide_content = """# 🚀 Streamlit Cloud Deployment Guide

## Quick Deployment Steps

### 1. Prepare Your Repository
```bash
# Initialize git repository (if not already done)
git init
git add .
git commit -m "Initial commit"

# Push to GitHub
git remote add origin <your-github-repo-url>
git push -u origin main
```

### 2. Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository
5. Set the main file path to: `app.py`
6. Click "Deploy!"

### 3. Configure Environment Variables

In your Streamlit Cloud app settings, add these environment variables:

```
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_SESSION_TOKEN=your_session_token
ATHENA_DATABASE=your_database_name
ATHENA_TABLE=your_table_name
ATHENA_S3_STAGING_DIR=s3://your-bucket/athena-results/
ATHENA_REGION=us-east-1
```

### 4. Update Table Name

Before deployment, update the table name in `athena_connector.py`:

```python
# Change this line in the get_sample_data method
FROM {ATHENA_DATABASE}.flight_delays_table
# To your actual table name
FROM {ATHENA_DATABASE}.your_actual_table_name
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure all dependencies are in `requirements.txt`
2. **AWS Connection**: Verify your AWS credentials and permissions
3. **Table Not Found**: Check your database and table names
4. **S3 Access**: Ensure your S3 bucket is accessible and configured correctly

### Debug Mode

To run in debug mode locally:
```bash
streamlit run app.py --logger.level debug
```

## Security Notes

- Never commit AWS credentials to your repository
- Use environment variables for sensitive data
- Consider using AWS IAM roles for production deployments
- Regularly rotate your AWS access keys

## Performance Tips

- Use specific filters to reduce query costs
- Set appropriate result limits
- Monitor your Athena query costs
- Consider implementing query result caching
"""
    
    with open("DEPLOYMENT_GUIDE.md", "w") as f:
        f.write(guide_content.strip())
    
    print("✅ Created DEPLOYMENT_GUIDE.md")

def main():
    """Main deployment preparation function"""
    print("🚀 Preparing Flight Delays Portal for deployment...")
    
    try:
        create_streamlit_config()
        create_env_template()
        update_config_for_deployment()
        create_deployment_guide()
        
        print("\n✅ Deployment preparation complete!")
        print("\n📋 Next steps:")
        print("1. Update your actual database and table names in athena_connector.py")
        print("2. Commit your changes to git")
        print("3. Push to GitHub")
        print("4. Deploy to Streamlit Cloud")
        print("5. Configure environment variables in Streamlit Cloud")
        print("\n📖 See DEPLOYMENT_GUIDE.md for detailed instructions")
        
    except Exception as e:
        print(f"❌ Error during deployment preparation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 