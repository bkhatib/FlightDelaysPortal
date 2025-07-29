#!/usr/bin/env python3
"""
Setup script for Flight Delays Portal
This script helps users configure and test the application
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def create_config_template():
    """Create a configuration template"""
    print("⚙️  Creating configuration template...")
    
    config_template = '''# Flight Delays Portal Configuration
# Update these values with your actual AWS and Athena settings

# AWS Credentials (replace with your actual values)
AWS_ACCESS_KEY_ID = "your_access_key_here"
AWS_SECRET_ACCESS_KEY = "your_secret_key_here"
AWS_SESSION_TOKEN = "your_session_token_here"

# Athena Configuration
ATHENA_DATABASE = "your_database_name"  # Replace with your database name
ATHENA_TABLE = "your_table_name"        # Replace with your table name
ATHENA_S3_STAGING_DIR = "s3://your-bucket/athena-results/"  # Replace with your S3 bucket
ATHENA_REGION = "us-east-1"  # Replace with your AWS region
'''
    
    with open("config_template.py", "w") as f:
        f.write(config_template)
    
    print("✅ Configuration template created: config_template.py")
    print("📝 Please update config.py with your actual values")

def run_tests():
    """Run connection tests"""
    print("🧪 Running connection tests...")
    try:
        result = subprocess.run([sys.executable, "test_connection.py"], 
                              capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Test execution failed: {e}")
        return False

def start_application():
    """Start the Streamlit application"""
    print("🚀 Starting Streamlit application...")
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Failed to start application: {e}")

def main():
    """Main setup function"""
    print("✈️  Flight Delays Portal Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Setup failed during dependency installation")
        sys.exit(1)
    
    # Create configuration template
    create_config_template()
    
    # Check if config.py exists and has been configured
    if os.path.exists("config.py"):
        print("\n📋 Configuration check:")
        with open("config.py", "r") as f:
            content = f.read()
            if "your_database_name" in content or "your_table_name" in content:
                print("⚠️  Please update config.py with your actual database and table names")
                print("   - Replace 'your_database_name' with your actual database name")
                print("   - Replace 'your_table_name' with your actual table name")
                print("   - Update S3 staging directory if needed")
            else:
                print("✅ Configuration appears to be set up")
    
    # Offer to run tests
    print("\n🧪 Would you like to run connection tests? (y/n): ", end="")
    response = input().lower().strip()
    if response in ['y', 'yes']:
        run_tests()
    
    # Offer to start the application
    print("\n🚀 Would you like to start the application now? (y/n): ", end="")
    response = input().lower().strip()
    if response in ['y', 'yes']:
        start_application()
    
    print("\n✅ Setup complete!")
    print("\n📖 Next steps:")
    print("1. Update config.py with your actual AWS and Athena settings")
    print("2. Run 'python test_connection.py' to test your connection")
    print("3. Run 'streamlit run app.py' to start the application")
    print("4. For deployment, see DEPLOYMENT_GUIDE.md")

if __name__ == "__main__":
    main() 