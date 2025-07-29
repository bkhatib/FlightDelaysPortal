import pandas as pd
import boto3
import os
import streamlit as st
from config import (
    AWS_ACCESS_KEY_ID, 
    AWS_SECRET_ACCESS_KEY, 
    AWS_SESSION_TOKEN,
    ATHENA_DATABASE,
    ATHENA_TABLE,
    ATHENA_S3_STAGING_DIR,
    ATHENA_REGION,
    ATHENA_CATALOG,
    ATHENA_SCHEMA,
    ATHENA_WORKGROUP
)

class AthenaConnector:
    def __init__(self):
        # Create AWS session with Athena credentials
        self.athena_session = boto3.Session(
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            aws_session_token=AWS_SESSION_TOKEN,
            region_name=ATHENA_REGION
        )
        
        # Initialize Athena client
        self.athena_client = self.athena_session.client('athena')
        self.output_location = ATHENA_S3_STAGING_DIR
    
    def execute_athena_query(self, query):
        """Execute a query using boto3 Athena client with pagination"""
        try:
            # Start query execution
            response = self.athena_client.start_query_execution(
                QueryString=query,
                QueryExecutionContext={
                    'Database': ATHENA_DATABASE
                },
                ResultConfiguration={
                    'OutputLocation': self.output_location
                }
            )
            
            query_execution_id = response['QueryExecutionId']
            
            # Wait for query completion
            import time
            while True:
                status_response = self.athena_client.get_query_execution(QueryExecutionId=query_execution_id)
                status = status_response['QueryExecution']['Status']['State']
                
                if status in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
                    break
                    
                time.sleep(2)
            
            if status == 'SUCCEEDED':
                # Get all results using pagination
                all_rows = []
                next_token = None
                
                while True:
                    if next_token:
                        results = self.athena_client.get_query_results(
                            QueryExecutionId=query_execution_id,
                            NextToken=next_token
                        )
                    else:
                        results = self.athena_client.get_query_results(QueryExecutionId=query_execution_id)
                    
                    # Extract column names from first call
                    if not all_rows:
                        columns = [col['Label'] for col in results['ResultSet']['ResultSetMetadata']['ColumnInfo']]
                    
                    # Extract data rows (skip header on first call)
                    start_idx = 1 if not all_rows else 0
                    for row in results['ResultSet']['Rows'][start_idx:]:
                        data_row = []
                        for data in row['Data']:
                            data_row.append(data.get('VarCharValue', ''))
                        all_rows.append(data_row)
                    
                    # Check if there are more results
                    next_token = results.get('NextToken')
                    if not next_token:
                        break
                
                # Create DataFrame
                if all_rows:
                    df = pd.DataFrame(all_rows, columns=columns)
                    return df
                else:
                    return pd.DataFrame()
            else:
                error_info = status_response['QueryExecution']['Status'].get('StateChangeReason', 'No error details')
                st.error(f"Query failed: {error_info}")
                return None
                
        except Exception as e:
            st.error(f"Query execution failed: {str(e)}")
            return None
    
    def execute_query(self, query):
        """Execute a query and return results as pandas DataFrame"""
        return self.execute_athena_query(query)
    
    def build_filtered_query(self, filters):
        """Build a filtered query based on user inputs with partition optimization"""
        base_query = f"""
        SELECT flight_code, origin, destination, dep_delayed, cal_dep_delayed_minutes, 
               scheduled_departure_date_time_utc, actual_departure_date_utc, journey_type, 
               order_c, selling_price_sum, gbv_sum, departure_date
        FROM {ATHENA_DATABASE}.{ATHENA_TABLE}
        WHERE departure_date IS NOT NULL
        """
        
        # Always add partition filters for optimal performance
        if filters.get('date_from'):
            base_query += f" AND departure_date >= '{filters['date_from']}'"
        if filters.get('date_to'):
            base_query += f" AND departure_date <= '{filters['date_to']}'"
        
        # Add other filters
        if filters.get('journey_type'):
            base_query += f" AND journey_type = '{filters['journey_type']}'"
        if filters.get('origin'):
            base_query += f" AND origin = '{filters['origin']}'"
        if filters.get('destination'):
            base_query += f" AND destination = '{filters['destination']}'"
        if filters.get('flight_code'):
            base_query += f" AND flight_code = '{filters['flight_code']}'"
        if filters.get('dep_delayed'):
            base_query += self._build_delay_filter(filters['dep_delayed'])
        
        # Add ordering with larger limit for display (50,000 records)
        base_query += " ORDER BY order_c LIMIT 50000"
        
        return base_query
    
    def _build_delay_filter(self, delay_range):
        """Build delay filter based on range"""
        if delay_range == 'Less than 15 minutes':
            return " AND CAST(dep_delayed AS DECIMAL(10,2)) < 15"
        elif delay_range == '15-30 minutes':
            return " AND CAST(dep_delayed AS DECIMAL(10,2)) >= 15 AND CAST(dep_delayed AS DECIMAL(10,2)) < 30"
        elif delay_range == '30-60 minutes':
            return " AND CAST(dep_delayed AS DECIMAL(10,2)) >= 30 AND CAST(dep_delayed AS DECIMAL(10,2)) < 60"
        elif delay_range == '60-90 minutes':
            return " AND CAST(dep_delayed AS DECIMAL(10,2)) >= 60 AND CAST(dep_delayed AS DECIMAL(10,2)) < 90"
        elif delay_range == 'More than 90 minutes':
            return " AND CAST(dep_delayed AS DECIMAL(10,2)) > 90"
        else:
            return ""
    
    def get_sample_data(self):
        """Get sample data from the table"""
        query = f"""
        SELECT flight_code, origin, destination, dep_delayed, cal_dep_delayed_minutes, 
               scheduled_departure_date_time_utc, actual_departure_date_utc, journey_type, 
               order_c, selling_price_sum, gbv_sum, departure_date
        FROM {ATHENA_DATABASE}.{ATHENA_TABLE}
        LIMIT 10
        """
        return self.execute_query(query)
    
    def get_unique_values(self, column_name):
        """Get unique values for a specific column"""
        query = f"""
        SELECT DISTINCT {column_name} 
        FROM {ATHENA_DATABASE}.{ATHENA_TABLE}
        WHERE {column_name} IS NOT NULL 
        ORDER BY {column_name}
        """
        return self.execute_query(query)
    
    def get_data_summary(self):
        """Get data summary with partition information"""
        query = f"""
        SELECT 
            COUNT(*) as total_records,
            COUNT(DISTINCT departure_date) as unique_dates,
            MIN(departure_date) as earliest_date,
            MAX(departure_date) as latest_date,
            COUNT(DISTINCT origin) as unique_origins,
            COUNT(DISTINCT destination) as unique_destinations,
            COUNT(DISTINCT flight_code) as unique_flights
        FROM {ATHENA_DATABASE}.{ATHENA_TABLE}
        """
        return self.execute_query(query) 

    def get_filtered_count(self, filters):
        """Get total count of records matching filters (without LIMIT)"""
        base_query = f"""
        SELECT COUNT(*) as total_count
        FROM {ATHENA_DATABASE}.{ATHENA_TABLE}
        WHERE departure_date IS NOT NULL
        """
        
        # Always add partition filters for optimal performance
        if filters.get('date_from'):
            base_query += f" AND departure_date >= '{filters['date_from']}'"
        if filters.get('date_to'):
            base_query += f" AND departure_date <= '{filters['date_to']}'"
        
        # Add other filters
        if filters.get('journey_type'):
            base_query += f" AND journey_type = '{filters['journey_type']}'"
        if filters.get('origin'):
            base_query += f" AND origin = '{filters['origin']}'"
        if filters.get('destination'):
            base_query += f" AND destination = '{filters['destination']}'"
        if filters.get('flight_code'):
            base_query += f" AND flight_code = '{filters['flight_code']}'"
        if filters.get('dep_delayed'):
            base_query += self._build_delay_filter(filters['dep_delayed'])
        
        return self.execute_query(base_query) 

    def get_filtered_metrics(self, filters):
        """Get aggregated metrics for records matching filters (without LIMIT)"""
        base_query = f"""
        SELECT 
            COUNT(*) as total_count,
            AVG(CAST(dep_delayed AS DECIMAL(10,2))) as avg_delay,
            SUM(CAST(order_c AS DECIMAL(10,2))) as total_orders,
            SUM(CAST(selling_price_sum AS DECIMAL(10,2))) as total_revenue
        FROM {ATHENA_DATABASE}.{ATHENA_TABLE}
        WHERE departure_date IS NOT NULL
        """
        
        # Always add partition filters for optimal performance
        if filters.get('date_from'):
            base_query += f" AND departure_date >= '{filters['date_from']}'"
        if filters.get('date_to'):
            base_query += f" AND departure_date <= '{filters['date_to']}'"
        
        # Add other filters
        if filters.get('journey_type'):
            base_query += f" AND journey_type = '{filters['journey_type']}'"
        if filters.get('origin'):
            base_query += f" AND origin = '{filters['origin']}'"
        if filters.get('destination'):
            base_query += f" AND destination = '{filters['destination']}'"
        if filters.get('flight_code'):
            base_query += f" AND flight_code = '{filters['flight_code']}'"
        if filters.get('dep_delayed'):
            base_query += self._build_delay_filter(filters['dep_delayed'])
        
        return self.execute_query(base_query) 

    def get_all_filtered_data(self, filters):
        """Get all records matching filters (without LIMIT) for export using pagination"""
        # First, get the total count
        count_query = f"""
        SELECT COUNT(*) as total_count
        FROM {ATHENA_DATABASE}.{ATHENA_TABLE}
        WHERE departure_date IS NOT NULL
        """
        
        # Always add partition filters for optimal performance
        if filters.get('date_from'):
            count_query += f" AND departure_date >= '{filters['date_from']}'"
        if filters.get('date_to'):
            count_query += f" AND departure_date <= '{filters['date_to']}'"
        
        # Add other filters
        if filters.get('journey_type'):
            count_query += f" AND journey_type = '{filters['journey_type']}'"
        if filters.get('origin'):
            count_query += f" AND origin = '{filters['origin']}'"
        if filters.get('destination'):
            count_query += f" AND destination = '{filters['destination']}'"
        if filters.get('flight_code'):
            count_query += f" AND flight_code = '{filters['flight_code']}'"
        if filters.get('dep_delayed'):
            count_query += self._build_delay_filter(filters['dep_delayed'])
        
        count_df = self.execute_query(count_query)
        total_count = int(count_df.iloc[0]['total_count']) if count_df is not None and not count_df.empty else 0
        
        if total_count == 0:
            return pd.DataFrame()
        
        # Use pagination to get all data
        all_data = []
        batch_size = 10000  # Process in batches of 10,000
        offset = 0
        
        while offset < total_count:
            # Build query with pagination
            base_query = f"""
            SELECT flight_code, origin, destination, dep_delayed, cal_dep_delayed_minutes, 
                   scheduled_departure_date_time_utc, actual_departure_date_utc, journey_type, 
                   order_c, selling_price_sum, gbv_sum, departure_date
            FROM {ATHENA_DATABASE}.{ATHENA_TABLE}
            WHERE departure_date IS NOT NULL
            """
            
            # Always add partition filters for optimal performance
            if filters.get('date_from'):
                base_query += f" AND departure_date >= '{filters['date_from']}'"
            if filters.get('date_to'):
                base_query += f" AND departure_date <= '{filters['date_to']}'"
            
            # Add other filters
            if filters.get('journey_type'):
                base_query += f" AND journey_type = '{filters['journey_type']}'"
            if filters.get('origin'):
                base_query += f" AND origin = '{filters['origin']}'"
            if filters.get('destination'):
                base_query += f" AND destination = '{filters['destination']}'"
            if filters.get('flight_code'):
                base_query += f" AND flight_code = '{filters['flight_code']}'"
            if filters.get('dep_delayed'):
                base_query += self._build_delay_filter(filters['dep_delayed'])
            
            # Add ordering and pagination
            base_query += f" ORDER BY order_c LIMIT {batch_size} OFFSET {offset}"
            
            batch_df = self.execute_query(base_query)
            if batch_df is not None and not batch_df.empty:
                all_data.append(batch_df)
                offset += len(batch_df)
            else:
                break
        
        # Combine all batches
        if all_data:
            return pd.concat(all_data, ignore_index=True)
        else:
            return pd.DataFrame() 