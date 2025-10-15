# Mega Dashboard

A lightweight, single-file dashboard application for monitoring statistics from multiple websites. Built with vanilla JavaScript, HTML, and CSS - **no build tools, no dependencies, no complexity**.

## Features

- 📊 **Real-time Stats Monitoring**: View statistics from all your websites at a glance
- 🔧 **Easy Management**: Add, edit, and delete websites through an intuitive UI
- 💾 **Local Storage**: Website configurations are stored locally in your browser
- 🎨 **Modern UI**: Clean and responsive design
- 🔄 **Auto-fetch**: Automatically fetches stats when websites are added
- ⚡ **Fast & Lightweight**: Pure vanilla JS - no build step, no node_modules, no frameworks
- 🚀 **Instant**: Just open the HTML file in your browser

## Stats Tracked

For each website, the dashboard displays:
- Published Articles
- Unpublished Articles
- Unused Ideas
- Hours Since Last Published
- Unread Messages

## Getting Started

### Super Simple Setup

1. **Clone the repository:**
```bash
git clone <repository-url>
cd mega-dashboard
```

2. **Open the file:**
   - Double-click `index.html`, or
   - Open it in your browser, or
   - Use a local server:
   ```bash
   python3 -m http.server 8000
   # Then open http://localhost:8000
   ```

That's it! No `npm install`, no build step, no configuration.

### Using with a Local Server (Optional)

If you want to test with a local server (useful for CORS testing):

```bash
# Python 3
python3 -m http.server 8000

# PHP
php -S localhost:8000

# Node.js (if you have npx)
npx serve
```

## 🔐 Authentication

The dashboard is protected with password + OTP (One-Time Password) authentication for security.

### Default Credentials:
- **Password:** `admin123`
- **OTP (4-digit code):** `1234`

**⚠️ IMPORTANT:** Change these default credentials before deploying!

### To Change Credentials:

Edit the `AUTH_CONFIG` object at the top of the `<script>` section in `index.html`:

```javascript
const AUTH_CONFIG = {
    password: 'your_secure_password',  // Change this
    otp: '9876',                       // Change this to your 4-digit code
    sessionDuration: 72 * 60 * 60 * 1000 // 72 hours
};
```

### Authentication Features:
- ✅ **Dual Authentication** - Requires both password and OTP code
- ✅ **72-hour session** - Stay logged in for 3 days automatically
- ✅ **Hacker-themed login** - Matrix-style green terminal design
- ✅ **Encrypted Storage** - All website data is encrypted with your password+OTP
- ✅ **XOR Encryption** - Data is unreadable without correct credentials
- ✅ **Auto-migrate** - Automatically encrypts old unencrypted data on first login
- ✅ **Session encryption** - Even auth tokens are encrypted
- ✅ **Memory cleanup** - Sensitive data cleared on logout
- ✅ **Auto-expire** - Session automatically expires after 72 hours
- ✅ **Logout button** - Located in top-right corner of dashboard

### Security:
- 🔒 **Server-side encryption** - All data encrypted on the server with AES-128 (Fernet)
- 🔒 **PBKDF2 key derivation** - 100,000 iterations for strong key generation
- 🔒 **Unique salts** - Each user's data has unique encryption salt
- 🔒 **No plain text storage** - Everything encrypted before saving to disk
- 🔒 **Secure sessions** - Cryptographically random tokens
- 🔒 **Search engine protection** - Multiple layers prevent indexing
- 🔒 **Security headers** - X-Frame-Options, CSP, X-Content-Type-Options
- 🔒 **Localhost only** - Server binds to 127.0.0.1 by default
- ⚠️ **Change credentials** - Always change default password and OTP!

## Usage

### Adding a Website

1. Navigate to the **Management** tab
2. Click **Add Website**
3. Fill in the details:
   - **Domain**: The full URL (e.g., `https://example.com`)
   - **API Key**: Your API authentication key (e.g., `mgapi_...`)
4. Click **Add Website**

The domain will automatically have `/api/v1/stats` appended when fetching statistics. The website name will be automatically fetched from the API response (`siteName` field).

### Viewing Statistics

1. Navigate to the **Dashboard** tab
2. Stats are automatically fetched when the page loads
3. Click **Refresh Stats** to manually update the statistics

### Editing a Website

1. Go to the **Management** tab
2. Click **Edit** next to the website you want to modify
3. Update the details and click **Update Website**

### Deleting a Website

1. Go to the **Management** tab
2. Click **Delete** next to the website
3. Confirm the deletion

## API Format

Your API endpoints should return JSON in one of these formats:

**Format 1 (Nested):**
```json
{
  "success": true,
  "siteName": "My Awesome Site",
  "stats": {
    "publishedArticles": 150,
    "unpublishedArticles": 5,
    "unusedIdeas": 23,
    "hoursSinceLastPublished": 12,
    "unreadMessages": 3
  },
  "timestamp": "2025-10-13T18:11:41.700Z"
}
```

**Format 2 (Flat):**
```json
{
  "siteName": "My Awesome Site",
  "publishedArticles": 150,
  "unpublishedArticles": 5,
  "unusedIdeas": 23,
  "hoursSinceLastPublished": 12,
  "unreadMessages": 3
}
```

**Required fields:**
- `siteName` - The name of your website (displayed in the dashboard)
- `publishedArticles` - Number of published articles
- `unpublishedArticles` - Number of unpublished articles
- `unusedIdeas` - Number of unused ideas
- `hoursSinceLastPublished` - Hours since last article was published
- `unreadMessages` - Number of unread messages

The dashboard supports both formats - stats can be nested in a `stats` object or at the root level.

The API endpoint should be accessible at: `{domain}/api/v1/stats`

Authentication header format: `Authorization: Bearer {apiKey}`

## Example API Request

```bash
curl https://mega-generator-production.up.railway.app/api/v1/stats \
  -H "Authorization: Bearer mgapi_47f57e769256f904285a0d58ad1608844d03d9b20699b8443c68a394c0174323"
```

## Technology

- **HTML5** - Structure
- **CSS3** - Styling (no frameworks)
- **Vanilla JavaScript** - Functionality (no libraries)
- **LocalStorage API** - Data persistence
- **Fetch API** - HTTP requests

## File Structure

```
mega-dashboard/
├── index.html          # The entire application (one file!)
└── README.md           # This file
```

## Benefits of This Approach

✅ **Zero dependencies** - No package.json, no node_modules  
✅ **No build step** - Edit and refresh, that's it  
✅ **Fast** - Opens instantly, no compilation  
✅ **Simple** - One file, ~500 lines total  
✅ **Portable** - Works anywhere, just copy the HTML file  
✅ **No version conflicts** - Pure web standards  
✅ **Easy to customize** - All code in one place  
✅ **Works offline** - Can be saved locally and works without a server  

## Browser Compatibility

Works in all modern browsers:
- Chrome/Edge 90+
- Firefox 88+
- Safari 14+

## Deployment

### GitHub Pages
1. Push to GitHub
2. Enable GitHub Pages in repository settings
3. Done! Your dashboard is live

### Any Static Host
Just upload `index.html` to:
- Netlify
- Vercel
- Cloudflare Pages
- Any web server

### Local Use
Just open the HTML file - no server needed!

## Security Note

- API keys are stored in browser localStorage
- Don't commit your API keys to the repository
- The dashboard runs entirely in your browser (client-side)
- No data is sent to any third-party servers

## Customization

All styles are in the `<style>` tag in the HTML file. Want to change colors, fonts, or layout? Just edit the CSS directly!

## Contributing

Contributions are welcome! The entire app is in one file, so it's easy to understand and modify.

## License

MIT License - feel free to use this project for personal or commercial purposes.
