# 🚀 Quick Start Guide

Get your Flight Delays Portal up and running in minutes!

## ⚡ Quick Setup (5 minutes)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Update Configuration
Edit `config.py` and replace the placeholder values:
```python
ATHENA_DATABASE = "your_actual_database_name"
ATHENA_TABLE = "your_actual_table_name"
ATHENA_S3_STAGING_DIR = "s3://your-bucket/athena-results/"
ATHENA_REGION = "your-aws-region"
```

### 3. Test Connection
```bash
python test_connection.py
```

### 4. Start Application
```bash
streamlit run app.py
```

## 🎯 What You'll Get

- **Interactive Data Table** with all your flight delays data
- **Powerful Filters**:
  - Date range selection
  - Journey type (INT/DOM)
  - Origin/Destination airports
  - Flight code search
  - Delay ranges (<15, 15-30, 30-60, 60-90, >90 min)
- **Sorting** by any column (orders, delays, revenue, etc.)
- **Analytics Dashboard** with charts and metrics
- **CSV Export** functionality

## 🔧 Configuration Details

### Required AWS Permissions
Your AWS credentials need access to:
- Athena: `StartQueryExecution`, `GetQueryExecution`, `GetQueryResults`
- Glue: `GetTable`, `GetTables`, `GetDatabase`, `GetDatabases`
- S3: `GetBucketLocation`, `GetObject`, `ListBucket`, `PutObject`

### Data Schema
Your Athena table should have these columns:
- `join_key`, `flight_code`, `origin`, `destination`
- `dep_delayed`, `journey_type`, `order_c`
- `selling_price_sum`, `gbv_sum`, `departure_date`
- `scheduled_departure_date_time_utc`, `actual_departure_date_utc`

## 🚀 Deployment to Streamlit Cloud

1. **Push to GitHub**
2. **Go to [share.streamlit.io](https://share.streamlit.io)**
3. **Connect your repository**
4. **Set main file to `app.py`**
5. **Add environment variables**:
   ```
   AWS_ACCESS_KEY_ID=your_key
   AWS_SECRET_ACCESS_KEY=your_secret
   AWS_SESSION_TOKEN=your_token
   ATHENA_DATABASE=your_db
   ATHENA_TABLE=your_table
   ATHENA_S3_STAGING_DIR=s3://your-bucket/results/
   ATHENA_REGION=your-region
   ```

## 🆘 Troubleshooting

### Common Issues

**"No data found"**
- Check your database and table names
- Verify AWS credentials have proper permissions
- Ensure your S3 bucket is accessible

**"Connection failed"**
- Verify AWS credentials are correct
- Check if your session token is expired
- Ensure Athena workgroup is configured

**"Import errors"**
- Run `pip install -r requirements.txt`
- Check Python version (3.8+ required)

### Getting Help

1. Run `python test_connection.py` for diagnostics
2. Check the full [README.md](README.md) for detailed instructions
3. Review [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for deployment help

## 🎉 You're Ready!

Once running, you'll have a powerful flight delays analytics portal with:
- Real-time data from your Athena database
- Interactive filtering and sorting
- Beautiful visualizations
- Export capabilities

Happy analyzing! ✈️ 