import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
from athena_connector import AthenaConnector
from config import ATHENA_DATABASE, ATHENA_TABLE
import base64
import io

# Set page config at the top level
st.set_page_config(
    page_title="Flight Delays Portal",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .filter-section {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=600)  # Cache for 10 minutes
def get_unique_values(column_name):
    """Get unique values for a specific column with partition optimization"""
    try:
        connector = AthenaConnector()
        result = connector.get_unique_values(column_name)
        if result is not None and not result.empty:
            return result[column_name].tolist()
        return []
    except Exception as e:
        st.error(f"Error getting unique values for {column_name}: {str(e)}")
        return []

@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_data_summary():
    """Get data summary with partition information"""
    try:
        connector = AthenaConnector()
        result = connector.get_data_summary()
        if result is not None and not result.empty:
            return result.iloc[0].to_dict()
        return {}
    except Exception as e:
        st.error(f"Error getting data summary: {str(e)}")
        return {}

def main():
    # Custom CSS
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .partition-info {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ff7f0e;
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<h1 class="main-header">✈️ Flight Delays Portal</h1>', unsafe_allow_html=True)
    
    # Data Summary Section
    with st.expander("📊 Data Summary & Partition Information", expanded=False):
        summary = get_data_summary()
        if summary:
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                total_records = int(summary.get('total_records', 0))
                st.metric("Total Records", f"{total_records:,}")
            with col2:
                unique_dates = int(summary.get('unique_dates', 0))
                st.metric("Unique Dates", f"{unique_dates:,}")
            with col3:
                unique_origins = int(summary.get('unique_origins', 0))
                st.metric("Unique Origins", f"{unique_origins:,}")
            with col4:
                unique_destinations = int(summary.get('unique_destinations', 0))
                st.metric("Unique Destinations", f"{unique_destinations:,}")
            
            st.markdown("")
    
    # Sidebar filters
    st.sidebar.header("🔍 Filters")
    

    
    date_from = st.sidebar.date_input(
        "From Date",
        value=None,
        help="Filter by departure date (partitioned column for optimal performance)"
    )
    
    date_to = st.sidebar.date_input(
        "To Date", 
        value=None,
        help="Filter by departure date (partitioned column for optimal performance)"
    )
    
    # Other filters
    st.sidebar.subheader("✈️ Flight Details")
    
    journey_types = ['All'] + get_unique_values('journey_type')
    journey_type = st.sidebar.selectbox("Journey Type", journey_types)
    
    origins = ['All'] + get_unique_values('origin')
    origin = st.sidebar.selectbox("Origin", origins)
    
    destinations = ['All'] + get_unique_values('destination')
    destination = st.sidebar.selectbox("Destination", destinations)
    
    flight_code = st.sidebar.text_input("Flight Code", placeholder="e.g., QR-1117")
    
    # Departure delay filter
    delay_options = [
        'All', 
        'Less than 15 minutes', 
        '15-30 minutes', 
        '30-60 minutes', 
        '60-90 minutes', 
        'More than 90 minutes'
    ]
    dep_delayed = st.sidebar.selectbox("Departure Delay", delay_options)
    
    # Apply filters button
    if st.sidebar.button("🚀 Apply Filters", type="primary"):
        # Build filters dictionary
        filters = {}
        if date_from:
            # Convert Python date object to string format YYYY-MM-DD
            filters['date_from'] = date_from.strftime('%Y-%m-%d')
        if date_to:
            # Convert Python date object to string format YYYY-MM-DD
            filters['date_to'] = date_to.strftime('%Y-%m-%d')
        if journey_type != 'All':
            filters['journey_type'] = journey_type
        if origin != 'All':
            filters['origin'] = origin
        if destination != 'All':
            filters['destination'] = destination
        if flight_code:
            filters['flight_code'] = flight_code
        if dep_delayed != 'All':
            filters['dep_delayed'] = dep_delayed
        
        # Execute query
        with st.spinner("🔄 Loading data..."):
            connector = AthenaConnector()
            df = connector.execute_query(connector.build_filtered_query(filters))
            
            if df is not None and not df.empty:
                displayed_count = len(df)
                
                # Display metrics
                metrics_df = connector.get_filtered_metrics(filters)
                
                # Get metrics from total dataset
                if metrics_df is not None and not metrics_df.empty:
                    total_count = int(metrics_df.iloc[0]['total_count'])
                    avg_delay = float(metrics_df.iloc[0]['avg_delay']) if metrics_df.iloc[0]['avg_delay'] is not None else 0
                    total_orders = float(metrics_df.iloc[0]['total_orders']) if metrics_df.iloc[0]['total_orders'] is not None else 0
                    total_revenue = float(metrics_df.iloc[0]['total_revenue']) if metrics_df.iloc[0]['total_revenue'] is not None else 0
                else:
                    total_count = displayed_count
                    avg_delay = 0
                    total_orders = 0
                    total_revenue = 0
                
                # Show pagination information
                if total_count > displayed_count:
                    st.success(f"✅ Showing {displayed_count:,} of {total_count:,} total records")
                else:
                    st.success(f"✅ Showing all {displayed_count:,} records")
                
                # Display metrics
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Records", f"{total_count:,}", f"Showing {displayed_count:,}")
                with col2:
                    st.metric("Avg Delay (min)", f"{avg_delay:.1f}" if avg_delay > 0 else "N/A")
                with col3:
                    st.metric("Total Orders", f"{total_orders:,.0f}" if total_orders > 0 else "N/A")
                with col4:
                    st.metric("Total Revenue", f"SAR {total_revenue:,.2f}" if total_revenue > 0 else "N/A")
                
                # Display data
                st.subheader("📋 Flight Delays Data")
                st.dataframe(df, use_container_width=True)
                
                # Simple download
                st.subheader("📥 Download Data")
                
                # Download displayed data (1000 records)
                csv_data = df.to_csv(index=False)
                
                st.download_button(
                    label=f"📥 Download Data ({len(df):,} records)",
                    data=csv_data,
                    file_name=f"flight_delays_{date_from}_{date_to}.csv",
                    mime="text/csv",
                    help="Download the complete dataset"
                )
                

            else:
                st.warning("⚠️ No data found for the selected filters. Try adjusting your criteria.")
    
    # Performance tips
    with st.sidebar.expander(""):
        st.markdown("")

if __name__ == "__main__":
    main() 