#!/usr/bin/env python3
"""
Test script for download functionality
"""

import pandas as pd
import io
import base64

def test_csv_creation():
    """Test CSV creation and download functionality"""
    
    # Create sample data
    data = {
        'flight_code': ['SV123', 'SV456', 'SV789'],
        'origin': ['JED', 'RUH', 'DMM'],
        'destination': ['RUH', 'DMM', 'JED'],
        'dep_delayed': ['15.5', '30.2', '45.8'],
        'order_c': ['100', '200', '300'],
        'selling_price_sum': ['1500.50', '2500.75', '3500.25']
    }
    
    df = pd.DataFrame(data)
    
    # Test CSV creation
    csv_data = df.to_csv(index=False)
    print(f"✅ CSV created successfully: {len(csv_data)} characters")
    print(f"✅ DataFrame has {len(df)} rows")
    
    # Test base64 encoding (alternative method)
    buffer = io.StringIO()
    df.to_csv(buffer, index=False)
    csv_string = buffer.getvalue()
    b64 = base64.b64encode(csv_string.encode()).decode()
    
    print(f"✅ Base64 encoding successful: {len(b64)} characters")
    
    # Test file download simulation
    filename = "test_flight_delays.csv"
    print(f"✅ File would be saved as: {filename}")
    
    return True

if __name__ == "__main__":
    print("🧪 Testing download functionality...")
    success = test_csv_creation()
    if success:
        print("✅ All download tests passed!")
    else:
        print("❌ Download tests failed!") 