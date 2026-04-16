import unittest
import sqlite3
import os
# 📦 Importing your secure application module
from frank_secure_auth import app, init_db

class FrankSecureAuthTest(unittest.TestCase):

    def setUp(self):
        """
        🚀 [INITIALIZATION] 🚀
        Standard Setup: Initializing the secure test environment.
        """
        self.app = app.test_client()
        self.app.testing = True
        # 🛡️ Using a separate test vault to ensure zero data corruption
        app.config['DATABASE'] = 'frank_test_vault.db'
        init_db()

    def test_home_page(self):
        """
        🌐 [NETWORK CHECK] 🌐
        Verifying the application's availability (HTTP 200 OK).
        """
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)

    def test_successful_login(self):
        """
        🔑 [AUTH CHECK] 🔑
        Testing authentication with encrypted credentials and hashed passwords.
        """
        response = self.app.post('/login', data={
            'username': 'admin', 
            'password': 'FrankTCRACyberchampion2026!'
        }, follow_redirects=True)
        # ✅ Asserting successful login via cryptographic verification
        self.assertIn(b'Authentication Successful', response.data)

    def test_sql_injection_prevention(self):
        """
        ⚔️ [SECURITY AUDIT] ⚔️
        Penetration Test: Verifying mitigation against SQL Injection (SQLi) attacks.
        """
        # 🔥 Simulation of an 'OR 1=1' malicious payload
        payload = "' OR '1'='1"
        response = self.app.post('/login', data={
            'username': payload, 
            'password': 'any_password'
        }, follow_redirects=True)
        
        # 🚫 EXPECTED: System must block the injection and return failure
        self.assertIn(b'Authentication Failed', response.data)

if __name__ == '__main__':
    # 🎯 Executing Frank's Champion Security Tests
    unittest.main()