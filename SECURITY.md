# Security Documentation

## 🔐 Security Features

### Search Engine Protection

The dashboard is protected from search engine indexing through multiple layers:

1. **robots.txt** - Instructs all search engines not to index
2. **Meta tags** - HTML meta tags prevent indexing
3. **X-Robots-Tag headers** - Server-side headers block crawlers
4. **No external links** - Prevents accidental exposure

### Server-Side Encryption

All sensitive data is encrypted on the server using industry-standard encryption:

- **PBKDF2** - Key derivation with 100,000 iterations
- **Fernet (AES-128)** - Symmetric encryption
- **SHA-256** - Secure hashing
- **Random salts** - Unique per user
- **Secure tokens** - Cryptographically random session tokens

### Data Protection

1. **At Rest**
   - All website data encrypted before saving to disk
   - Passwords, API keys, and domains are encrypted
   - Each user has separate encrypted file

2. **In Transit**
   - Use HTTPS in production (recommend nginx reverse proxy)
   - Session tokens transmitted via headers
   - No sensitive data in URLs

3. **In Memory**
   - Data only decrypted when needed
   - Cleared on logout
   - Session expiry after 72 hours

### Authentication

- **Dual factor** - Password + OTP required
- **Session management** - Server-side session validation
- **Token-based** - Secure random tokens
- **Expiry** - Automatic session expiration

## ⚠️ Important Security Notes

### Change Default Credentials

**CRITICAL:** Change the default credentials in `server.py`:

```python
DEFAULT_PASSWORD = 'your_secure_password_here'
DEFAULT_OTP = '9876'
```

### Network Security

The server binds to `127.0.0.1` (localhost only) by default. This means:

- ✅ Only accessible from the same machine
- ✅ Not exposed to network
- ✅ Protected from remote attacks

To access from network (NOT RECOMMENDED without HTTPS):
```python
app.run(host='0.0.0.0', port=5000)  # WARNING: Only with HTTPS!
```

### Production Deployment

For production use:

1. **Use HTTPS** - Set up SSL/TLS certificates
2. **Reverse Proxy** - Use nginx or Apache
3. **Firewall** - Restrict access by IP
4. **Environment Variables** - Use .env file (never commit it!)
5. **Strong Credentials** - Use long, random passwords
6. **Regular Updates** - Keep dependencies updated

### File Permissions

Secure the data directory:

```bash
chmod 700 secure_data/
chmod 600 secure_data/*.enc
```

### Backup Security

If backing up encrypted data:
- ✅ Encrypted files are safe to backup
- ✅ Useless without credentials
- ⚠️ Keep backups secure anyway
- ⚠️ Never backup credentials with data

## 🔒 Best Practices

1. **Strong Credentials**
   - Use password managers
   - Minimum 12 characters
   - Mix of letters, numbers, symbols

2. **Access Control**
   - Limit who has credentials
   - Don't share OTP codes
   - Use unique credentials per deployment

3. **Regular Audits**
   - Review access logs
   - Check for unauthorized access
   - Update credentials periodically

4. **Secure Environment**
   - Keep server physically secure
   - Use full disk encryption
   - Secure backup locations

## 🚨 If Credentials Are Compromised

1. Stop the server immediately
2. Change `DEFAULT_PASSWORD` and `DEFAULT_OTP` in `server.py`
3. Delete `secure_data/sessions.json`
4. Restart the server
5. All existing sessions will be invalidated

## 📝 Audit Log

Consider implementing:
- Login attempt logging
- Failed authentication tracking
- Data access logging
- Session management logging

## Additional Hardening

For maximum security:

1. **Rate Limiting** - Prevent brute force
2. **IP Whitelisting** - Only allow specific IPs
3. **2FA/MFA** - Add time-based OTP (TOTP)
4. **Encrypted Sessions** - Encrypt session storage
5. **Database** - Move to proper database with encryption
6. **HSM** - Use hardware security module for key storage

---

**Remember:** Security is a process, not a product. Stay vigilant!

