import tkinter as tk
from tkinter import messagebox
from pysqlcipher3 import dbapi2 as sqlite3
import hashlib
import re
from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class LoginApp:
    # Read DB_PASSWORD from environment, with secure default for development
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'dev_password_change_in_production')
    
    def __init__(self, root):
        self.root = root
        self.root.title("Login Application")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")
        
        # Warn if using default password
        if self.DB_PASSWORD == 'dev_password_change_in_production':
            print("⚠️  WARNING: Using default database password. This is insecure!")
            print("   Set DB_PASSWORD environment variable for production use.")
        
        # Center window on screen
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'+{x}+{y}')
        
        self.init_db()
        self.show_login_screen()

    def init_db(self):
        """Initialize encrypted SQLite database"""
        db_path = Path("users.db")
        self.conn = sqlite3.connect(str(db_path))
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

    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()

    def validate_email(self, email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def validate_password(self, password):
        """Validate password strength"""
        if len(password) < 6:
            return False, "Password must be at least 6 characters"
        if not any(char.isdigit() for char in password):
            return False, "Password must contain at least one digit"
        if not any(char.isupper() for char in password):
            return False, "Password must contain at least one uppercase letter"
        return True, "Valid"

    def clear_frame(self):
        """Clear all widgets from the frame"""
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_login_screen(self):
        """Display login screen"""
        self.clear_frame()
        
        frame = tk.Frame(self.root, bg="#f0f0f0")
        frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        # Title
        title = tk.Label(frame, text="Login", font=("Arial", 24, "bold"), bg="#f0f0f0")
        title.pack(pady=20)
        
        # Username
        tk.Label(frame, text="Username:", font=("Arial", 10), bg="#f0f0f0").pack(anchor="w", pady=(10, 0))
        self.login_username = tk.Entry(frame, font=("Arial", 10), width=30)
        self.login_username.pack(pady=(0, 15), ipady=5)
        
        # Password
        tk.Label(frame, text="Password:", font=("Arial", 10), bg="#f0f0f0").pack(anchor="w", pady=(10, 0))
        self.login_password = tk.Entry(frame, font=("Arial", 10), width=30, show="*")
        self.login_password.pack(pady=(0, 20), ipady=5)
        
        # Login button
        login_btn = tk.Button(frame, text="Login", font=("Arial", 11, "bold"), 
                             bg="#4CAF50", fg="white", width=20, padx=10, pady=8,
                             command=self.login)
        login_btn.pack(pady=10)
        
        # Register button
        register_btn = tk.Button(frame, text="Create New Account", font=("Arial", 11), 
                                bg="#2196F3", fg="white", width=20, padx=10, pady=8,
                                command=self.show_register_screen)
        register_btn.pack(pady=5)

    def show_register_screen(self):
        """Display registration screen"""
        self.clear_frame()
        
        frame = tk.Frame(self.root, bg="#f0f0f0")
        frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        # Title
        title = tk.Label(frame, text="Register", font=("Arial", 24, "bold"), bg="#f0f0f0")
        title.pack(pady=20)
        
        # Username
        tk.Label(frame, text="Username:", font=("Arial", 10), bg="#f0f0f0").pack(anchor="w", pady=(10, 0))
        self.reg_username = tk.Entry(frame, font=("Arial", 10), width=30)
        self.reg_username.pack(pady=(0, 15), ipady=5)
        
        # Email
        tk.Label(frame, text="Email:", font=("Arial", 10), bg="#f0f0f0").pack(anchor="w", pady=(10, 0))
        self.reg_email = tk.Entry(frame, font=("Arial", 10), width=30)
        self.reg_email.pack(pady=(0, 15), ipady=5)
        
        # Password
        tk.Label(frame, text="Password:", font=("Arial", 10), bg="#f0f0f0").pack(anchor="w", pady=(10, 0))
        self.reg_password = tk.Entry(frame, font=("Arial", 10), width=30, show="*")
        self.reg_password.pack(pady=(0, 15), ipady=5)
        
        # Confirm Password
        tk.Label(frame, text="Confirm Password:", font=("Arial", 10), bg="#f0f0f0").pack(anchor="w", pady=(10, 0))
        self.reg_confirm = tk.Entry(frame, font=("Arial", 10), width=30, show="*")
        self.reg_confirm.pack(pady=(0, 20), ipady=5)
        
        # Register button
        reg_btn = tk.Button(frame, text="Register", font=("Arial", 11, "bold"), 
                           bg="#4CAF50", fg="white", width=20, padx=10, pady=8,
                           command=self.register)
        reg_btn.pack(pady=10)
        
        # Back button
        back_btn = tk.Button(frame, text="Back to Login", font=("Arial", 11), 
                            bg="#FF9800", fg="white", width=20, padx=10, pady=8,
                            command=self.show_login_screen)
        back_btn.pack(pady=5)

    def login(self):
        """Handle login"""
        username = self.login_username.get().strip()
        password = self.login_password.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Username and password are required")
            return
        
        hashed_password = self.hash_password(password)
        
        try:
            self.cursor.execute(
                "SELECT * FROM users WHERE username = ? AND password = ?",
                (username, hashed_password)
            )
            user = self.cursor.fetchone()
            
            if user:
                messagebox.showinfo("Success", f"Welcome, {username}!")
                self.show_dashboard(username)
            else:
                messagebox.showerror("Error", "Invalid username or password")
        except Exception as e:
            messagebox.showerror("Error", f"Login failed: {str(e)}")

    def register(self):
        """Handle registration"""
        username = self.reg_username.get().strip()
        email = self.reg_email.get().strip()
        password = self.reg_password.get()
        confirm = self.reg_confirm.get()
        
        if not username or not email or not password or not confirm:
            messagebox.showerror("Error", "All fields are required")
            return
        
        if not self.validate_email(email):
            messagebox.showerror("Error", "Invalid email format")
            return
        
        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match")
            return
        
        is_valid, message = self.validate_password(password)
        if not is_valid:
            messagebox.showerror("Error", message)
            return
        
        hashed_password = self.hash_password(password)
        
        try:
            self.cursor.execute(
                "INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
                (username, hashed_password, email)
            )
            self.conn.commit()
            messagebox.showinfo("Success", "Account created successfully! Please login.")
            self.show_login_screen()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists")
        except Exception as e:
            messagebox.showerror("Error", f"Registration failed: {str(e)}")

    def show_dashboard(self, username):
        """Display dashboard after successful login"""
        self.clear_frame()
        
        frame = tk.Frame(self.root, bg="#f0f0f0")
        frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        # Welcome message
        welcome = tk.Label(frame, text=f"Welcome, {username}!", 
                          font=("Arial", 20, "bold"), bg="#f0f0f0", fg="#4CAF50")
        welcome.pack(pady=30)
        
        # Info
        info = tk.Label(frame, text="You have successfully logged in.", 
                       font=("Arial", 12), bg="#f0f0f0")
        info.pack(pady=10)
        
        # Logout button
        logout_btn = tk.Button(frame, text="Logout", font=("Arial", 11, "bold"), 
                              bg="#F44336", fg="white", width=20, padx=10, pady=8,
                              command=self.show_login_screen)
        logout_btn.pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()
