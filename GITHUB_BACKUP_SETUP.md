# 🔄 GitHub Automated Backup Setup

## Overview
This setup automatically backs up your encrypted dashboard data to GitHub using GitHub Actions. The backup runs daily at 2 AM UTC and can be triggered manually.

## 🚀 Quick Setup

### 1. Get Railway CLI Token
```bash
# Install Railway CLI (if not already installed)
npm install -g @railway/cli

# Login to Railway (this will open browser for authentication)
railway login

# Get your token from Railway dashboard
# Go to: https://railway.app/account/tokens
# Create a new token and copy it for GitHub secrets
```

**Alternative: Create token via Railway Dashboard**
1. Go to [Railway Account Tokens](https://railway.app/account/tokens)
2. Click **"Create Token"**
3. Give it a name like "GitHub Backup"
4. Copy the generated token

### 2. Configure GitHub Secrets
In your GitHub repository:

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Add these secrets:

| Secret Name | Value | Description |
|-------------|-------|-------------|
| `RAILWAY_TOKEN` | `railway_xxxxx` | Your Railway CLI token from step 1 |
| `RAILWAY_PROJECT_ID` | `your-project-id` | Your Railway project ID (found in Railway dashboard) |

### 3. Enable GitHub Actions
1. Go to your repository **Actions** tab
2. Click **I understand my workflows, go ahead and enable them**
3. The backup workflow will start automatically

## 📁 What Gets Backed Up

### ✅ **Included (Encrypted Data Only)**
- All `*.enc` files from `secure_data/` directory
- User-specific encrypted website data
- Backup metadata and timestamps

### ❌ **Excluded (Not Backed Up)**
- Session files (`sessions.json`)
- Lockout data (`lockouts.json`)
- Login attempt logs (`login_attempts.log`)
- Temporary files

## 🔧 Backup Schedule

### **Automatic Backups**
- **Daily at 2 AM UTC** (configurable in workflow)
- **Retention**: 30 days (old backups auto-deleted)
- **Compression**: Files stored as-is (already encrypted)

### **Manual Backups**
- Trigger via GitHub Actions tab
- Click "Run workflow" button
- Immediate backup creation

## 📊 Storage Usage

### **Typical Usage**
- **Per backup**: ~1-5MB (encrypted files only)
- **Monthly total**: ~30-150MB
- **GitHub free limit**: 1GB (plenty of space)

### **Cost**
- **GitHub**: Free (within limits)
- **Railway**: No additional cost
- **Actions**: ~5 minutes per backup

## 🔍 Monitoring Backups

### **Check Backup Status**
1. Go to **Actions** tab in your repository
2. Look for "Backup Encrypted Dashboard Data" workflow
3. Green checkmark = successful backup
4. Red X = backup failed

### **View Backup Files**
1. Navigate to `backups/` folder in your repository
2. Each backup is in a timestamped directory
3. Files include:
   - `*.enc` - Your encrypted data files
   - `backup_manifest.json` - Backup metadata

### **Backup Verification**
Each backup includes:
- File count verification
- Size verification
- Integrity checks
- Timestamp and metadata

## 🚨 Troubleshooting

### **Common Issues**

#### **Backup Fails - "No encrypted files found"**
- **Cause**: No websites added to dashboard yet
- **Solution**: Add at least one website to generate encrypted data
- **Status**: Normal if dashboard is empty

#### **Backup Fails - "Railway login failed"**
- **Cause**: Invalid `RAILWAY_TOKEN` secret
- **Solution**: 
  1. Go to [Railway Account Tokens](https://railway.app/account/tokens)
  2. Create a new token or copy existing one
  3. Update `RAILWAY_TOKEN` secret in GitHub

#### **Backup Fails - "Project not found"**
- **Cause**: Invalid `RAILWAY_PROJECT_ID` secret
- **Solution**: 
  1. Check Railway dashboard for correct project ID
  2. Update `RAILWAY_PROJECT_ID` secret in GitHub

### **Manual Backup Verification**
```bash
# Check if backup API works
curl -H "Authorization: Bearer YOUR_TOKEN" \
     https://your-railway-app.railway.app/api/backup-info
```

## 🔄 Recovery Process

### **Restore from Backup**
1. **Download backup** from GitHub `backups/` folder
2. **Extract encrypted files** to local directory
3. **Upload to Railway** (if needed):
   ```bash
   railway run --service web mkdir -p secure_data
   railway run --service web cp *.enc secure_data/
   ```

### **Verify Recovery**
1. Login to your dashboard
2. Check if websites are restored
3. Verify data integrity

## ⚙️ Customization

### **Change Backup Schedule**
Edit `.github/workflows/backup.yml`:
```yaml
schedule:
  - cron: '0 2 * * *'  # Daily at 2 AM UTC
  # - cron: '0 */6 * * *'  # Every 6 hours
  # - cron: '0 0 * * 0'    # Weekly on Sunday
```

### **Change Retention Period**
Edit the cleanup section:
```yaml
# Keep only last 30 days (change number as needed)
find backups/ -type d -mtime +30 -exec rm -rf {} +
```

### **Add Notifications**
Add email/Slack notifications on backup success/failure.

## 🔐 Security

### **Data Protection**
- ✅ **Encrypted files only**: Raw data never exposed
- ✅ **Private repository**: Backup data stays private
- ✅ **Access control**: Only you can access backups
- ✅ **Git history**: Version control for all backups

### **No Sensitive Data**
- Session tokens not backed up
- Login credentials not backed up
- Only encrypted website data backed up

## 📈 Benefits

- **Automated**: No manual intervention needed
- **Reliable**: GitHub Actions infrastructure
- **Versioned**: Git history for all backups
- **Free**: No additional costs
- **Secure**: Encrypted data only
- **Accessible**: Easy to download and restore

---

🎉 **Your encrypted dashboard data is now automatically backed up to GitHub!**
