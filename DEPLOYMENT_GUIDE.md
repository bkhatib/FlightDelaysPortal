# 🚀 Deployment Guide - Flight Delays Portal

## Prerequisites

- GitHub account
- Streamlit Cloud account (free at [share.streamlit.io](https://share.streamlit.io))
- AWS credentials with Athena access

## Step 1: Push to GitHub

1. **Initialize Git repository** (if not already done):
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Flight Delays Portal"
   ```

2. **Create a new repository on GitHub** and push your code:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/FlightDelaysPortal.git
   git branch -M main
   git push -u origin main
   ```

## Step 2: Deploy to Streamlit Cloud

1. **Go to [share.streamlit.io](https://share.streamlit.io)**
2. **Sign in with GitHub**
3. **Click "New app"**
4. **Configure your app**:
   - **Repository**: Select your `FlightDelaysPortal` repository
   - **Branch**: `main`
   - **Main file path**: `app.py`
   - **App URL**: Choose a custom URL (optional)

## Environment Variables Setup

In Streamlit Cloud, add these environment variables:

```toml
AWS_ACCESS_KEY_ID = "YOUR_AWS_ACCESS_KEY_ID"
AWS_SECRET_ACCESS_KEY = "YOUR_AWS_SECRET_ACCESS_KEY"
AWS_SESSION_TOKEN = "YOUR_AWS_SESSION_TOKEN"
ATHENA_DATABASE = "l1_almosafer"
ATHENA_TABLE = "fact_flight_delay_scheduler"
ATHENA_S3_STAGING_DIR = "s3://aws-athena-query-results-032862061730-eu-west-1/"
ATHENA_REGION = "eu-west-1"
ATHENA_CATALOG = "awsdatacatalog"
ATHENA_SCHEMA = "l1_almosafer"
ATHENA_WORKGROUP = "primary"
```

**Note**: Replace the AWS credentials with your actual values. Never commit real credentials to the repository.

## Step 4: Deploy

1. **Click "Deploy!"**
2. **Wait for deployment** (usually takes 1-2 minutes)
3. **Your app will be live** at the provided URL

## Step 5: Test Your Deployment

1. **Open your deployed app URL**
2. **Test the filters**:
   - Date range selection
   - Journey type (INT/DOM)
   - Origin/Destination
   - Flight code
   - Departure delay ranges
3. **Verify data loading** and sorting functionality

## Troubleshooting

### Common Issues:

1. **"Module not found" errors**:
   - Check that `requirements.txt` is in your repository
   - Verify all dependencies are listed

2. **AWS connection errors**:
   - Verify environment variables are set correctly
   - Check that AWS credentials are valid and not expired
   - Ensure the region is correct (`eu-west-1`)

3. **"Schema not found" errors**:
   - Verify `ATHENA_DATABASE` is set to `l1_almosafer`
   - Check that `ATHENA_REGION` is set to `eu-west-1`

### Updating Credentials:

If your AWS session token expires, you'll need to:
1. Generate new credentials from AWS
2. Update the environment variables in Streamlit Cloud
3. Redeploy the app

## Security Notes

- **Never commit credentials to Git**
- **Use environment variables** for all sensitive data
- **Consider using AWS IAM roles** for production deployments
- **Rotate credentials regularly**

## Performance Tips

- The app caches queries for 10 minutes
- Use specific filters to reduce query time
- Consider implementing pagination for large datasets

## Support

If you encounter issues:
1. Check the Streamlit Cloud logs
2. Verify your AWS credentials and permissions
3. Test the connection locally first
4. Review the troubleshooting section in the README

## Next Steps

After successful deployment:
1. **Share the app URL** with your team
2. **Monitor usage** and performance
3. **Consider adding authentication** if needed
4. **Set up monitoring** for AWS costs

---

🎉 **Congratulations! Your Flight Delays Portal is now live on Streamlit Cloud!** 