# 🚀 Railway Deployment Guide

## Prerequisites
- Railway account (free tier available)
- GitHub repository with your code

## Deployment Steps

### 1. Prepare Your Repository
```bash
# Ensure all files are committed
git add .
git commit -m "Prepare for Railway deployment"
git push origin main
```

### 2. Deploy to Railway

#### Option A: GitHub Integration (Recommended)
1. Go to [Railway.app](https://railway.app)
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository
5. Railway will automatically detect the Python app

#### Option B: Railway CLI
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Initialize project
railway init

# Deploy
railway up
```

### 3. Configure Environment Variables

In your Railway dashboard, go to Variables and add:

```
DASHBOARD_PASSWORD=your_secure_password_here
DASHBOARD_OTP=your_4_digit_code_here
```

**⚠️ IMPORTANT**: Never use default credentials in production!

### 4. Custom Domain (Optional)

1. In Railway dashboard, go to Settings → Domains
2. Add your custom domain
3. Railway will provide DNS records to configure

## Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `DASHBOARD_PASSWORD` | Dashboard login password | Yes | `admin123` |
| `DASHBOARD_OTP` | 4-digit OTP code | Yes | `1234` |
| `PORT` | Server port | No | `5001` |

## Security Features

✅ **Server-side encryption** with AES-128 (Fernet)
✅ **PBKDF2 key derivation** (100k iterations)
✅ **Rate limiting** (5 attempts, 15min lockout)
✅ **Secure sessions** with cryptographic tokens
✅ **Security headers** (no caching, no indexing)
✅ **CORS protection**

## Monitoring

Railway provides built-in monitoring:
- **Logs**: View real-time logs in dashboard
- **Metrics**: CPU, memory, and network usage
- **Health checks**: Automatic restart on failure

## Troubleshooting

### Common Issues

1. **App won't start**
   - Check environment variables are set
   - Verify `requirements.txt` is present
   - Check logs in Railway dashboard

2. **Cannot login**
   - Ensure `DASHBOARD_PASSWORD` and `DASHBOARD_OTP` are set
   - Check credentials match your .env file

3. **Data not persisting**
   - Railway provides persistent storage by default
   - Data is encrypted and stored securely

### Logs
```bash
# View logs via Railway CLI
railway logs

# Or check Railway dashboard → Deployments → View Logs
```

## Backup & Recovery

Your encrypted data is stored in Railway's persistent storage. To backup:

1. **Export via API**: Use the dashboard to export data
2. **Database backup**: Railway handles this automatically
3. **Manual backup**: Download encrypted files from Railway dashboard

## Scaling

Railway automatically scales based on traffic:
- **Free tier**: 512MB RAM, 1GB storage
- **Pro tier**: Higher limits and custom domains
- **Auto-scaling**: Handles traffic spikes automatically

## Support

- **Railway Docs**: https://docs.railway.app
- **Community**: Railway Discord
- **Status**: https://status.railway.app

---

🎉 **Your secure dashboard is now deployed and accessible worldwide!**
