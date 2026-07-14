import unittest
import os
import tempfile
import shutil
from pathlib import Path
import sys

# Mock tkinter for testing
try:
    import tkinter as tk
except ImportError:
    class MockTk:
        pass
    sys.modules['tkinter'] = MockTk()
    sys.modules['tkinter.messagebox'] = MockTk()

from pysqlcipher3 import dbapi2 as sqlite3
import hashlib
import re


class TestPasswordValidation(unittest.TestCase):
    """Test password validation logic"""
    
    def test_password_too_short(self):
        """Test password with less than 6 characters"""
        password = "Pass1"
        result = self.validate_password(password)
        self.assertFalse(result[0])
        self.assertIn("6 characters", result[1])
    
    def test_password_missing_digit(self):
        """Test password without digit"""
        password = "PasswordAbc"
        result = self.validate_password(password)
        self.assertFalse(result[0])
        self.assertIn("digit", result[1])
    
    def test_password_missing_uppercase(self):
        """Test password without uppercase letter"""
        password = "password1"
        result = self.validate_password(password)
        self.assertFalse(result[0])
        self.assertIn("uppercase", result[1])
    
    def test_valid_password(self):
        """Test valid password"""
        password = "ValidPass123"
        result = self.validate_password(password)
        self.assertTrue(result[0])
    
    @staticmethod
    def validate_password(password):
        """Validate password strength"""
        if len(password) < 6:
            return False, "Password must be at least 6 characters"
        if not any(char.isdigit() for char in password):
            return False, "Password must contain at least one digit"
        if not any(char.isupper() for char in password):
            return False, "Password must contain at least one uppercase letter"
        return True, "Valid"


class TestEmailValidation(unittest.TestCase):
    """Test email validation logic"""
    
    def test_valid_email(self):
        """Test valid email addresses"""
        valid_emails = [
            "user@example.com",
            "test.user@domain.co.uk",
            "first_last+tag@example.org"
        ]
        for email in valid_emails:
            result = self.validate_email(email)
            self.assertTrue(result, f"Email {email} should be valid")
    
    def test_invalid_email(self):
        """Test invalid email addresses"""
        invalid_emails = [
            "userexample.com",
            "user@",
            "@example.com",
            "user @example.com",
            "user@.com"
        ]
        for email in invalid_emails:
            result = self.validate_email(email)
            self.assertFalse(result, f"Email {email} should be invalid")
    
    @staticmethod
    def validate_email(email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None


class TestPasswordHashing(unittest.TestCase):
    """Test password hashing"""
    
    def test_hash_consistency(self):
        """Test that same password produces same hash"""
        password = "TestPassword123"
        hash1 = self.hash_password(password)
        hash2 = self.hash_password(password)
        self.assertEqual(hash1, hash2)
    
    def test_different_passwords_different_hashes(self):
        """Test that different passwords produce different hashes"""
        password1 = "TestPassword123"
        password2 = "TestPassword124"
        hash1 = self.hash_password(password1)
        hash2 = self.hash_password(password2)
        self.assertNotEqual(hash1, hash2)
    
    def test_hash_length(self):
        """Test SHA-256 hash is 64 characters"""
        password = "TestPassword123"
        hash_result = self.hash_password(password)
        self.assertEqual(len(hash_result), 64)
    
    @staticmethod
    def hash_password(password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()


class TestDatabaseOperations(unittest.TestCase):
    """Test encrypted database operations"""
    
    DB_PASSWORD = "test_db_password_2024"
    
    def setUp(self):
        """Create temporary database for testing"""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test.db")
        self.init_db()
    
    def tearDown(self):
        """Clean up temporary database"""
        if hasattr(self, 'conn'):
            self.conn.close()
        shutil.rmtree(self.temp_dir)
    
    def init_db(self):
        """Initialize encrypted database"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.execute(f"PRAGMA key='{self.DB_PASSWORD}'")
        self.conn.execute("PRAGMA cipher_page_size = 4096")
        self.conn.execute("PRAGMA kdf_iter = 64000")
        self.cursor = self.conn.cursor()
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                email TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()
    
    def test_create_user(self):
        """Test creating a new user"""
        username = "testuser"
        password_hash = hashlib.sha256("TestPass123".encode()).hexdigest()
        email = "test@example.com"
        
        self.cursor.execute(
            "INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
            (username, password_hash, email)
        )
        self.conn.commit()
        
        self.cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = self.cursor.fetchone()
        self.assertIsNotNone(user)
        self.assertEqual(user[1], username)
        self.assertEqual(user[3], email)
    
    def test_duplicate_username(self):
        """Test that duplicate usernames are rejected"""
        username = "testuser"
        password_hash = hashlib.sha256("TestPass123".encode()).hexdigest()
        email = "test@example.com"
        
        self.cursor.execute(
            "INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
            (username, password_hash, email)
        )
        self.conn.commit()
        
        with self.assertRaises(sqlite3.IntegrityError):
            self.cursor.execute(
                "INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
                (username, password_hash, "other@example.com")
            )
            self.conn.commit()
    
    def test_retrieve_user(self):
        """Test retrieving a user by credentials"""
        username = "testuser"
        password = "TestPass123"
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        email = "test@example.com"
        
        self.cursor.execute(
            "INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
            (username, password_hash, email)
        )
        self.conn.commit()
        
        self.cursor.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username, password_hash)
        )
        user = self.cursor.fetchone()
        self.assertIsNotNone(user)
        self.assertEqual(user[1], username)
    
    def test_invalid_credentials(self):
        """Test retrieving user with invalid credentials"""
        username = "testuser"
        password = "TestPass123"
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        email = "test@example.com"
        
        self.cursor.execute(
            "INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
            (username, password_hash, email)
        )
        self.conn.commit()
        
        wrong_password_hash = hashlib.sha256("WrongPass123".encode()).hexdigest()
        self.cursor.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username, wrong_password_hash)
        )
        user = self.cursor.fetchone()
        self.assertIsNone(user)
    
    def test_database_encryption(self):
        """Test that database file is encrypted"""
        # Database should exist
        self.assertTrue(os.path.exists(self.db_path))
        
        # Try to read raw file (should be unreadable encrypted content)
        with open(self.db_path, 'rb') as f:
            content = f.read(16)
            # SQLite unencrypted files start with "SQLite format 3"
            self.assertNotEqual(content[:13], b'SQLite format')


class TestInputValidation(unittest.TestCase):
    """Test input validation"""
    
    def test_empty_username(self):
        """Test that empty username is invalid"""
        self.assertFalse(self._is_valid_input("", "password@123", "test@example.com"))
    
    def test_empty_password(self):
        """Test that empty password is invalid"""
        self.assertFalse(self._is_valid_input("username", "", "test@example.com"))
    
    def test_empty_email(self):
        """Test that empty email is invalid"""
        self.assertFalse(self._is_valid_input("username", "password@123", ""))
    
    def test_valid_inputs(self):
        """Test all valid inputs"""
        self.assertTrue(self._is_valid_input("username", "Password123", "test@example.com"))
    
    @staticmethod
    def _is_valid_input(username, password, email):
        """Validate input"""
        return bool(username and password and email)


if __name__ == '__main__':
    unittest.main()
