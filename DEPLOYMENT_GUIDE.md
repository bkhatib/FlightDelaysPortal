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

## Step 3: Set Environment Variables

In Streamlit Cloud, go to your app settings and add these environment variables:

### Required Environment Variables:

```
AWS_ACCESS_KEY_ID=ASIAQPJV3ISRLZ6XP7OH
AWS_SECRET_ACCESS_KEY=hgttADotkbRDgkJEPbsD8XYsXrG2MlR10lCH77GN
AWS_SESSION_TOKEN=IQoJb3JpZ2luX2VjEGUaCWV1LXdlc3QtMSJGMEQCIBUfg8C9q7EXqfGNqRifGCRqm3NWhW6sAWXdwPG/9NALAiAcoPGTP67E1Osk6MCl5VBhs/wNnZnE7aOjHWmZ8b1phiqUAwiN//////////8BEAIaDDAzMjg2MjA2MTczMCIMdbGzX3ePsx+BAoCeKugCD19/1C9YjbIPTMd7mypztTBIbw9bdIJmdTHYlzqLIbCCflqV+S/ari3KtfUgQ+9aKmPT436J9Q1vbaSE/h74VQuP9yzjZDPsyTqZTEjoEhMh00ChrCcfy+r7mojoznl/Dyf4pYqw2a6MqsHFDV6+vfp37Q0lSvo3gfANXu4xlpMyuOLF6MsvT1ze2Z0YIYGBeWdDnXp86b8QxbyPNSCPUfExL1O0CPvwXLsEoQ30VxzKqXFIVEmKru/zj6oRrqUz/dHXhiQlaM+LHQjazZ/J0lss2xQNJTdH+HxH2nmow/ABpS7MNNmXoQCihI2s+owQIRx34ctS1171F6i4MNxP0ooetmnkgg3Ctxv+i7yMIzQjVnfEJHygTPEt1TD5gVCwADxVASGIFewTvgysjqD+cxJUy/nhAumr3KqGqM1boCGGJ1ac8CbXd2mWz0jF3qf87zsQPsbn6+GkVUFY86k6Tp/3o+yUDlxgMPfSncQGOqcBoGPRgBY+yKdTxU93mSM7+fTcRi7RpTrLV0aTQx9tzTVgCDCskN6BWTZ0i4pYTuFoWiEAiMJiu6m41btZzamNlSz8qgZ1BdFKgLyjQlQzIO0AsQCWjahkiArd2KQGzMPX4d7aTo2dIAz6Z5z/qwedFssJF1IjC1c0ymtFTdKsA24XiX5rIi3XsbXnAlt05Sx+C/N842xXUpfeN0jvnKQbiPUBLSceEgs=
```

### Optional Environment Variables (if you want to override defaults):

```
ATHENA_DATABASE=l1_almosafer
ATHENA_TABLE=fact_flight_delay_scheduler
ATHENA_S3_STAGING_DIR=s3://aws-athena-query-results-032862061730-eu-west-1/
ATHENA_REGION=eu-west-1
ATHENA_CATALOG=awsdatacatalog
ATHENA_SCHEMA=l1_almosafer
ATHENA_WORKGROUP=primary
```

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