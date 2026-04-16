from flask import Flask, request, redirect, url_for, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

# 🚀 INITIALIZING THE FLASK ENGINE
app = Flask(__name__)

# 🔑 CRITICAL: Secret key for session integrity and flash messaging
# This must be stored in an environment variable in production environments.
app.secret_key = 'frank_secure_2026_top_3_alpha' 

# 🏛️ 1. DATABASE ARCHITECTURE (The Secure Foundation)
def init_db():
    """
    🛠️ FUNCTION: init_db
    PURPOSE: Initializes the secure vault and ensures robust user storage.
    """
    conn = sqlite3.connect('frank_vault.db')
    c = conn.cursor()
    
    # ✅ SECURITY LAYER: Using UNIQUE constraint to prevent account duplication
    # ⚡ PERFORMANCE: Ensuring INTEGER PRIMARY KEY for optimized indexing
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)''')

    # 💾 SEEDING ADMINISTRATIVE CREDENTIALS
    # 🛡️ DEFENSE: Implementing One-Way Hashing to mitigate 'Sensitive Data Exposure' (OWASP A02)
    # The plaintext password never touches the disk.
    admin_password = 'FrankTCRACyberchampion2026!'
    hashed_pw = generate_password_hash(admin_password)
    
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('admin', hashed_pw))
    except sqlite3.IntegrityError:
        # 🔍 STATUS: Admin entity already exists in the secure vault
        pass 

    conn.commit()
    conn.close()

# 🔐 2. SECURE AUTHENTICATION GATEWAY (Countering SQLi & Broken Auth)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_input = request.form.get('username')
        pass_input = request.form.get('password')

        conn = sqlite3.connect('frank_vault.db')
        c = conn.cursor()

        # ⚔️ DEFENSIVE STRATEGY: Parameterized Queries
        # This implementation annihilates SQL Injection (SQLi) risks by decoupling data from commands.
        c.execute("SELECT password FROM users WHERE username = ?", (user_input,)) 
        record = c.fetchone()
        conn.close()

        # 🧪 DEFENSIVE STRATEGY: Cryptographic Hash Verification
        # Validating the provided entropy against the stored cryptographic hash.
        if record and check_password_hash(record[0], pass_input):
            return "<h1>🚀 Authentication Successful. Welcome, Frank!</h1>"
        else:
            # 🛡️ MASKING ERROR: Generic response to prevent 'User Enumeration' attacks.
            return "<h2>❌ Authentication Failed. Invalid credentials.</h2>"

    # 🖥️ DEPLOYING SECURE FRONT-END INTERFACE
    return '''
        <style>
            body { background-color: #f0f2f5; font-family: sans-serif; text-align: center; padding-top: 50px; }
            form { background: white; padding: 20px; display: inline-block; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
            input { margin: 10px; padding: 10px; border-radius: 4px; border: 1px solid #ddd; }
            input[type="submit"] { background: #007bff; color: white; border: none; cursor: pointer; }
        </style>
        <h2>🛡️ Secure Login Portal 🛡️</h2>
        <form method="post">
            Username: <input type="text" name="username" required placeholder="Enter Identity"><br>
            Password: <input type="password" name="password" required placeholder="Enter Secret"><br>
            <input type="submit" value="Authorize Access">
        </form>
    '''

# 🏁 SYSTEM LAUNCHPAD
if __name__ == '__main__':
    # 🛠️ Self-check: Initialize the vault before engine start
    init_db() 
    
    # ⚠️ CRITICAL ALERT: debug must be set to False in production
    # This prevents stack trace leaks and Remote Code Execution (RCE) vulnerabilities.
    app.run(debug=False)