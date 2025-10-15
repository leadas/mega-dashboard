#!/usr/bin/env python3
"""
Secure Dashboard Server with Server-Side Encryption
This server provides proper encryption for sensitive data.
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json
import hashlib
import secrets
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__, static_folder='.')
CORS(app)

# Configuration
DATA_DIR = 'secure_data'
SESSIONS_FILE = os.path.join(DATA_DIR, 'sessions.json')
USERS_FILE = os.path.join(DATA_DIR, 'users.json')
LOCKOUTS_FILE = os.path.join(DATA_DIR, 'lockouts.json')
LOGIN_LOG_FILE = os.path.join(DATA_DIR, 'login_attempts.log')
SESSION_DURATION = 72 * 60 * 60  # 72 hours in seconds

# Rate Limiting Configuration
MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_DURATION = 15 * 60  # 15 minutes in seconds

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# Load credentials from environment variables (or use defaults for first-time setup)
DEFAULT_PASSWORD = os.getenv('DASHBOARD_PASSWORD', 'admin123')
DEFAULT_OTP = os.getenv('DASHBOARD_OTP', '1234')

# Warn if using default credentials
if DEFAULT_PASSWORD == 'admin123' or DEFAULT_OTP == '1234':
    print("⚠️  WARNING: Using default credentials! Create .env file with custom credentials.")


def derive_key(password: str, salt: bytes) -> bytes:
    """Derive encryption key from password using PBKDF2"""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))


def get_user_file(username: str) -> str:
    """Get user-specific data file path"""
    safe_username = hashlib.sha256(username.encode()).hexdigest()[:16]
    return os.path.join(DATA_DIR, f'{safe_username}.enc')


def load_sessions():
    """Load active sessions"""
    if os.path.exists(SESSIONS_FILE):
        try:
            with open(SESSIONS_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}


def save_sessions(sessions):
    """Save active sessions"""
    with open(SESSIONS_FILE, 'w') as f:
        json.dump(sessions, f)


def load_lockouts():
    """Load lockout data from disk"""
    if os.path.exists(LOCKOUTS_FILE):
        try:
            with open(LOCKOUTS_FILE, 'r') as f:
                data = json.load(f)
                # Convert ISO strings back to datetime
                for ip in data:
                    if data[ip].get('locked_until'):
                        data[ip]['locked_until'] = datetime.fromisoformat(data[ip]['locked_until'])
                return data
        except:
            return {}
    return {}


def save_lockouts(lockouts):
    """Save lockout data to disk (persistent)"""
    # Convert datetime to ISO string for JSON serialization
    serializable = {}
    for ip, data in lockouts.items():
        serializable[ip] = {
            'count': data['count'],
            'locked_until': data['locked_until'].isoformat() if data.get('locked_until') else None
        }
    
    with open(LOCKOUTS_FILE, 'w') as f:
        json.dump(serializable, f, indent=2)


def log_login_attempt(ip, success, message=''):
    """Log login attempts to file"""
    timestamp = datetime.now().isoformat()
    status = 'SUCCESS' if success else 'FAILED'
    
    with open(LOGIN_LOG_FILE, 'a') as f:
        f.write(f"{timestamp} | IP: {ip:15} | {status:7} | {message}\n")


def is_ip_locked(ip, lockouts):
    """Check if IP is currently locked out"""
    if ip not in lockouts:
        return False, None
    
    attempt = lockouts[ip]
    if attempt.get('locked_until'):
        if datetime.now() < attempt['locked_until']:
            # Still locked
            remaining = (attempt['locked_until'] - datetime.now()).total_seconds()
            return True, int(remaining)
        else:
            # Lockout expired, reset
            lockouts[ip] = {'count': 0, 'locked_until': None}
            save_lockouts(lockouts)
            return False, None
    return False, None


def record_failed_attempt(ip, lockouts):
    """Record failed login attempt and check if should lock"""
    if ip not in lockouts:
        lockouts[ip] = {'count': 0, 'locked_until': None}
    
    lockouts[ip]['count'] += 1
    
    if lockouts[ip]['count'] >= MAX_LOGIN_ATTEMPTS:
        lockouts[ip]['locked_until'] = datetime.now() + timedelta(seconds=LOCKOUT_DURATION)
        save_lockouts(lockouts)
        log_login_attempt(ip, False, f"LOCKED OUT - {MAX_LOGIN_ATTEMPTS} failed attempts")
        return True, LOCKOUT_DURATION
    
    save_lockouts(lockouts)
    remaining = MAX_LOGIN_ATTEMPTS - lockouts[ip]['count']
    log_login_attempt(ip, False, f"Invalid credentials - {remaining} attempts remaining")
    return False, remaining


def reset_attempts(ip, lockouts):
    """Reset failed attempts on successful login"""
    if ip in lockouts:
        lockouts[ip] = {'count': 0, 'locked_until': None}
        save_lockouts(lockouts)


def validate_session(token: str) -> bool:
    """Check if session token is valid"""
    sessions = load_sessions()
    if token not in sessions:
        return False
    
    session = sessions[token]
    expiry = datetime.fromisoformat(session['expires'])
    
    if datetime.now() > expiry:
        del sessions[token]
        save_sessions(sessions)
        return False
    
    return True


def get_session_username(token: str) -> str:
    """Get username from session token"""
    sessions = load_sessions()
    return sessions.get(token, {}).get('username')


@app.route('/')
def index():
    """Serve main page"""
    # Add security headers
    response = send_from_directory('.', 'index.html')
    response.headers['X-Robots-Tag'] = 'noindex, nofollow, noarchive, nosnippet'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    return response


@app.route('/api/login', methods=['POST'])
def login():
    """Authenticate user and create session with rate limiting"""
    ip = request.remote_addr
    lockouts = load_lockouts()
    
    # Check if IP is locked out
    is_locked, remaining_time = is_ip_locked(ip, lockouts)
    if is_locked:
        minutes = int(remaining_time / 60)
        seconds = int(remaining_time % 60)
        return jsonify({
            'success': False,
            'error': 'LOCKED',
            'message': f'Too many failed attempts. Locked for {minutes}m {seconds}s',
            'locked_until': remaining_time
        }), 429
    
    data = request.json
    password = data.get('password')
    otp = data.get('otp')
    
    # Validate credentials
    if password == DEFAULT_PASSWORD and otp == DEFAULT_OTP:
        # Success - reset attempts and create session
        reset_attempts(ip, lockouts)
        log_login_attempt(ip, True, 'Login successful')
        
        token = secrets.token_urlsafe(32)
        username = f"{password}:{otp}"
        
        sessions = load_sessions()
        sessions[token] = {
            'username': username,
            'created': datetime.now().isoformat(),
            'expires': (datetime.now() + timedelta(seconds=SESSION_DURATION)).isoformat()
        }
        save_sessions(sessions)
        
        return jsonify({
            'success': True,
            'token': token,
            'expires': sessions[token]['expires']
        })
    
    # Failed - record attempt
    locked, remaining = record_failed_attempt(ip, lockouts)
    
    if locked:
        return jsonify({
            'success': False,
            'error': 'LOCKED',
            'message': f'Account locked for 15 minutes due to {MAX_LOGIN_ATTEMPTS} failed attempts',
            'locked_until': LOCKOUT_DURATION
        }), 429
    
    return jsonify({
        'success': False,
        'error': 'Invalid credentials',
        'attempts_remaining': remaining
    }), 401


@app.route('/api/logout', methods=['POST'])
def logout():
    """Invalidate session"""
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    
    if token:
        sessions = load_sessions()
        if token in sessions:
            del sessions[token]
            save_sessions(sessions)
    
    return jsonify({'success': True})


@app.route('/api/data', methods=['GET'])
def get_data():
    """Retrieve encrypted user data"""
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    
    if not validate_session(token):
        print(f"[GET /api/data] Invalid session token")
        return jsonify({'error': 'Invalid or expired session'}), 401
    
    username = get_session_username(token)
    user_file = get_user_file(username)
    
    print(f"[GET /api/data] Username: {username}, File: {user_file}")
    
    if not os.path.exists(user_file):
        print(f"[GET /api/data] File not found, returning empty data")
        return jsonify({'data': []})
    
    # Read encrypted data
    with open(user_file, 'rb') as f:
        encrypted_data = f.read()
    
    print(f"[GET /api/data] Loaded {len(encrypted_data)} bytes from disk")
    
    # Derive key and decrypt
    salt = encrypted_data[:16]
    encrypted_content = encrypted_data[16:]
    
    key = derive_key(username, salt)
    fernet = Fernet(key)
    
    try:
        decrypted = fernet.decrypt(encrypted_content)
        data = json.loads(decrypted.decode())
        print(f"[GET /api/data] Successfully decrypted {len(data)} websites")
        return jsonify({'data': data})
    except Exception as e:
        print(f"[GET /api/data] Decryption failed: {e}")
        return jsonify({'error': 'Decryption failed'}), 500


@app.route('/api/data', methods=['POST'])
def save_data():
    """Save encrypted user data"""
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    
    if not validate_session(token):
        print(f"[POST /api/data] Invalid session token")
        return jsonify({'error': 'Invalid or expired session'}), 401
    
    username = get_session_username(token)
    user_file = get_user_file(username)
    
    data = request.json.get('data', [])
    
    print(f"[POST /api/data] Username: {username}, File: {user_file}")
    print(f"[POST /api/data] Saving {len(data)} websites")
    
    # Generate salt and derive key
    salt = secrets.token_bytes(16)
    key = derive_key(username, salt)
    fernet = Fernet(key)
    
    # Encrypt data
    json_data = json.dumps(data).encode()
    encrypted = fernet.encrypt(json_data)
    
    # Save salt + encrypted data
    with open(user_file, 'wb') as f:
        f.write(salt + encrypted)
    
    print(f"[POST /api/data] Successfully saved {len(encrypted)} bytes to disk")
    
    return jsonify({'success': True})


@app.route('/robots.txt')
def robots():
    """Serve robots.txt"""
    return send_from_directory('.', 'robots.txt', mimetype='text/plain')


@app.route('/favicon.ico')
def favicon():
    """Serve favicon"""
    try:
        return send_from_directory('.', 'favicon.ico', mimetype='image/x-icon')
    except:
        return '', 204  # No content


@app.route('/health')
def health_check():
    """Health check endpoint for Railway"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '2.1.0'
    }), 200


@app.route('/api/proxy-stats', methods=['POST'])
def proxy_stats():
    """Proxy endpoint to fetch stats from external websites (bypass CORS)"""
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    
    if not validate_session(token):
        return jsonify({'error': 'Invalid or expired session'}), 401
    
    data = request.json
    domain = data.get('domain')
    api_key = data.get('apiKey')
    
    if not domain or not api_key:
        return jsonify({'error': 'Missing domain or apiKey'}), 400
    
    try:
        # Fetch stats from external website
        response = requests.get(
            f"{domain}/api/v1/stats",
            headers={
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            },
            timeout=10
        )
        
        if not response.ok:
            return jsonify({
                'error': f'HTTP {response.status_code}: {response.reason}',
                'isOnline': False
            }), 200
        
        return jsonify({
            'data': response.json(),
            'isOnline': True
        })
    
    except requests.exceptions.Timeout:
        return jsonify({'error': 'Request timeout', 'isOnline': False}), 200
    except requests.exceptions.ConnectionError:
        return jsonify({'error': 'Connection failed', 'isOnline': False}), 200
    except Exception as e:
        return jsonify({'error': str(e), 'isOnline': False}), 200


if __name__ == '__main__':
    print("=" * 60)
    print("🔐 SECURE MEGA DASHBOARD SERVER")
    print("=" * 60)
    print(f"Server starting on http://localhost:5001")
    print(f"Data directory: {os.path.abspath(DATA_DIR)}")
    print()
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("⚠️  WARNING: No .env file found!")
        print("   Create .env file with your credentials")
        print("   See env.example for template")
        print()
    
    # Warn if using defaults
    if DEFAULT_PASSWORD == 'admin123':
        print("⚠️  WARNING: Using default password!")
    if DEFAULT_OTP == '1234':
        print("⚠️  WARNING: Using default OTP!")
    
    if DEFAULT_PASSWORD != 'admin123' and DEFAULT_OTP != '1234':
        print("✅ Custom credentials loaded from .env")
    
    print("=" * 60)
    
    # Run with security settings
    port = int(os.getenv('PORT', 5001))
    host = '0.0.0.0' if os.getenv('RAILWAY_ENVIRONMENT') else '127.0.0.1'
    
    app.run(
        host=host,
        port=port,
        debug=False,  # Never use debug in production
        threaded=True
    )

