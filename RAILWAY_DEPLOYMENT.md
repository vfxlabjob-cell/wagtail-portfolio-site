# Railway Deployment Guide for Wagtail Site

This guide will help you deploy your Wagtail site to Railway successfully.

## Prerequisites

1. A Railway account (https://railway.app/)
2. Your project pushed to a Git repository (GitHub, GitLab, or Bitbucket)
3. PostgreSQL database service on Railway

## Step 1: Create New Railway Project

1. Go to [Railway Dashboard](https://railway.app/dashboard)
2. Click "New Project"
3. Choose "Deploy from GitHub repo"
4. Select your repository
5. Railway will automatically detect this as a Python project

## Step 2: Add PostgreSQL Database

1. In your project dashboard, click "New Service"
2. Choose "Add Database" → "PostgreSQL"
3. Railway will automatically create a PostgreSQL instance and set the `DATABASE_URL` environment variable

## Step 3: Set Environment Variables

Go to your service → Variables tab and add these required variables:

### Required Variables

```bash
SECRET_KEY=your-super-secret-django-key-here-make-it-very-long-and-random
DEBUG=False
RAILWAY_ENVIRONMENT=production
```

### Generate a Secret Key

Run this locally to generate a secure secret key:
```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

### Optional Variables (for admin user creation)

```bash
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=your-secure-admin-password
```

### Optional Variables (for email functionality)

```bash
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### Optional Variables (for Cloudflare R2/AWS S3 media storage)

Only add these if you want to store media files in cloud storage:

```bash
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket-name
AWS_S3_ENDPOINT_URL=https://your-account-id.r2.cloudflarestorage.com
AWS_S3_CUSTOM_DOMAIN=your-custom-domain.com
```

## Step 4: Deploy

1. Railway will automatically start building and deploying your project
2. The build process includes:
   - Installing Python dependencies
   - Running database migrations
   - Collecting static files
   - Starting the Gunicorn server

## Step 5: Verify Deployment

1. Wait for the deployment to complete (usually 2-5 minutes)
2. Click on your service to see the public URL
3. Visit `https://your-app-name-production-xxxx.up.railway.app/health/` to check if the app is running
4. Visit `https://your-app-name-production-xxxx.up.railway.app/admin/` to access the Wagtail admin

## Troubleshooting

### Common Issues and Solutions

#### 1. Build Fails During Migration
**Error**: Database connection issues during `python manage.py migrate`

**Solution**: 
- Ensure PostgreSQL service is running
- Check that `DATABASE_URL` is set correctly
- Verify the database service is in the same project

#### 2. Health Check Fails
**Error**: "Service unavailable" during health check

**Solutions**:
- Check the application logs for Python/Django errors
- Ensure all environment variables are set correctly
- Verify the `SECRET_KEY` is set and not empty
- Check if migrations completed successfully

#### 3. Static Files Not Loading
**Error**: CSS/JS files return 404 errors

**Solution**:
- This is expected on first deploy - static files are served by WhiteNoise
- Check if `collectstatic` command completed successfully in logs

#### 4. Admin Panel Shows "Bad Request (400)"
**Error**: CSRF or Host header issues

**Solution**:
- Ensure `RAILWAY_PUBLIC_DOMAIN` is being set automatically by Railway
- Check `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` in settings

### Viewing Logs

1. Go to your Railway service
2. Click on "Deployments"
3. Click on the latest deployment
4. View build logs and runtime logs

### Key Log Messages to Look For

✅ **Success indicators:**
```
Applying database migrations...
Operations to perform: X migrations
Collecting static files...
Starting Gunicorn server on port 8000...
Production settings loaded:
- DEBUG: False
- DATABASE: PostgreSQL
```

❌ **Error indicators:**
```
django.core.exceptions.ImproperlyConfigured
ModuleNotFoundError
psycopg2.OperationalError
gunicorn.errors.HaltServer
```

## File Structure Overview

Your project should have these key files for Railway deployment:

```
wagtail_site/
├── railway.toml          # Railway configuration
├── requirements.txt      # Python dependencies
├── runtime.txt          # Python version specification
├── start.sh             # Startup script
└── mysite/
    ├── manage.py
    └── mysite/
        └── settings/
            └── production.py  # Production settings
```

## Post-Deployment

### Creating a Superuser

If you didn't set the `DJANGO_SUPERUSER_*` environment variables, you can create an admin user manually:

1. Go to Railway dashboard → your service
2. Click on "Connect" tab
3. Use the web-based terminal or connect via CLI
4. Run:
```bash
cd mysite
python manage.py createsuperuser --settings=mysite.settings.production
```

### Setting Up Your Site Content

1. Access the admin panel at `/admin/`
2. Go to Settings → Sites
3. Update the default site with your Railway domain
4. Add your content through the Wagtail admin interface

## Environment Variables Reference

| Variable | Required | Description |
|----------|----------|-------------|
| `SECRET_KEY` | Yes | Django secret key for cryptographic signing |
| `DATABASE_URL` | Yes | PostgreSQL connection string (auto-set by Railway) |
| `DEBUG` | No | Set to False for production (default: False) |
| `RAILWAY_PUBLIC_DOMAIN` | No | Your app domain (auto-set by Railway) |
| `DJANGO_SUPERUSER_USERNAME` | No | Auto-create superuser with this username |
| `DJANGO_SUPERUSER_EMAIL` | No | Email for auto-created superuser |
| `DJANGO_SUPERUSER_PASSWORD` | No | Password for auto-created superuser |

## Performance Tips

1. **Database Connection Pooling**: Railway PostgreSQL includes connection pooling
2. **Static Files**: WhiteNoise handles static file serving efficiently
3. **Workers**: The app uses 2 Gunicorn workers by default, suitable for most small to medium sites
4. **Caching**: Consider adding Redis for session/cache storage for higher traffic

## Security Considerations

1. Never commit sensitive environment variables to your repository
2. Use strong, random passwords for all accounts
3. Regularly update dependencies
4. Monitor Railway logs for suspicious activity
5. Consider setting up domain-specific `ALLOWED_HOSTS` instead of `*`

## Cost Optimization

1. **Starter Plan**: Usually sufficient for small Wagtail sites
2. **Resource Usage**: Monitor your app's memory and CPU usage
3. **Database Size**: Keep track of your PostgreSQL storage usage
4. **Scaling**: Railway auto-scales based on traffic

## Getting Help

1. **Railway Docs**: https://docs.railway.app/
2. **Railway Discord**: https://railway.app/discord
3. **Wagtail Docs**: https://docs.wagtail.org/
4. **Django Deployment**: https://docs.djangoproject.com/en/stable/howto/deployment/

---

## Quick Deployment Checklist

- [ ] Repository connected to Railway
- [ ] PostgreSQL service added
- [ ] `SECRET_KEY` environment variable set
- [ ] `DEBUG=False` environment variable set
- [ ] Optional superuser variables set
- [ ] Deployment completed successfully
- [ ] Health check passes (`/health/`)
- [ ] Admin panel accessible (`/admin/`)
- [ ] Site content configured

Good luck with your deployment! 🚀