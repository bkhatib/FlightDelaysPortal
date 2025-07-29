# Flight Delays Portal

A Streamlit application for analyzing flight delays data from AWS Athena with **partition optimization** for optimal performance.

## Features

- **Interactive Data Filtering**: Filter by date range, journey type, origin/destination, flight code, and departure delays
- **Sortable Data**: Sort by any column, especially `order_c`
- **Real-time Queries**: Direct connection to AWS Athena for live data
- **Responsive UI**: Modern, user-friendly interface
- **Partition Optimization**: Optimized queries using `departure_date` partitioning for better performance and cost efficiency

## Performance Optimizations

### 🔍 **Partition-Aware Queries**
- **Partitioned Column**: `departure_date` is partitioned for optimal performance
- **Query Optimization**: Date filters are applied first to leverage partition pruning
- **Cost Reduction**: Only scans relevant partitions, reducing Athena costs
- **Faster Queries**: Recent data queries are significantly faster

### 📊 **Smart Data Loading**
- **Recent Data Focus**: Unique value queries limited to recent data (30 days)
- **Sample Data**: Recent 7-day sample data for quick previews
- **Summary Statistics**: 90-day summary for overview metrics
- **Caching**: Results cached for 10 minutes to reduce repeated queries

## Setup

### Prerequisites

- Python 3.8+
- AWS Athena access
- Valid AWS credentials with Athena permissions

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd FlightDelaysPortal
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure AWS credentials**
   
   **IMPORTANT**: Make sure your AWS credentials have access to the same data as your Athena console.
   
   Update `config.py` with your AWS credentials:
   ```python
   AWS_ACCESS_KEY_ID = "your_access_key"
   AWS_SECRET_ACCESS_KEY = "your_secret_key"
   AWS_SESSION_TOKEN = "your_session_token"  # If using temporary credentials
   ```

4. **Configure Athena settings**
   ```python
   ATHENA_DATABASE = "l1_almosafer"
   ATHENA_TABLE = "fact_flight_delay_scheduler"
   ATHENA_S3_STAGING_DIR = "s3://aws-athena-query-results-032862061730-eu-west-1/"
   ATHENA_REGION = "eu-west-1"
   ```

### Troubleshooting

**If you get "SCHEMA_NOT_FOUND" errors:**

1. **Check that your API credentials match your console access**
   - Use the same AWS account/role as your Athena console
   - Ensure the credentials have the same permissions

2. **Verify your database and table names**
   - Check the exact names in your Athena console
   - Make sure the case matches exactly

3. **Test your credentials**
   ```bash
   python3 test_debug.py
   ```

## Running Locally

```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`

## Deployment to Streamlit Cloud

1. **Push your code to GitHub**
2. **Connect your repository to Streamlit Cloud**
3. **Set environment variables** in Streamlit Cloud:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
   - `AWS_SESSION_TOKEN` (if using temporary credentials)

## Data Schema

The application expects a table with the following columns:
- `departure_date`: Date of departure (**partitioned column**)
- `journey_type`: Type of journey
- `origin`: Origin airport
- `destination`: Destination airport
- `flight_code`: Flight code
- `dep_delayed`: Departure delay in minutes
- `order_c`: Order column for sorting

## Configuration

### Environment Variables

For deployment, set these environment variables:
- `AWS_ACCESS_KEY_ID`: Your AWS access key
- `AWS_SECRET_ACCESS_KEY`: Your AWS secret key
- `AWS_SESSION_TOKEN`: Your AWS session token (if using temporary credentials)

### Athena Configuration

- `ATHENA_DATABASE`: Your database name
- `ATHENA_TABLE`: Your table name
- `ATHENA_S3_STAGING_DIR`: S3 bucket for Athena results
- `ATHENA_REGION`: AWS region

## Performance & Cost Optimization

### 🚀 **Query Performance**
- **Partition Pruning**: Only scans relevant date partitions
- **Filter Optimization**: Date filters applied first for maximum efficiency
- **Caching**: Results cached for 10 minutes
- **Smart Limits**: Recent data queries for better performance

### 💰 **Cost Management**
- **Reduced Data Scans**: Partition filtering minimizes data scanned
- **Efficient Queries**: Optimized query structure reduces Athena costs
- **Caching Strategy**: Reduces repeated expensive queries
- **Date Range Limits**: Encourages users to specify date ranges

### 📈 **Best Practices**
1. **Always use date filters** for optimal performance
2. **Limit date ranges** to reduce scan costs
3. **Use specific filters** to minimize data scanned
4. **Monitor query costs** in AWS Athena console

## Customization

You can customize the application by:
- Modifying the filter options in `app.py`
- Adding new columns to the display
- Changing the styling in the CSS section
- Adjusting partition optimization strategies

## Security

- AWS credentials are stored securely
- No sensitive data is logged
- Use temporary credentials when possible
- Environment variables for all sensitive configuration

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify your AWS credentials and permissions
3. Test the connection using the provided test scripts
4. Review partition optimization best practices

## License

This project is licensed under the MIT License. 