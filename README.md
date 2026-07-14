# Windows Login Application

A complete login application built with Python and tkinter, packaged in Docker.

## Features

- User registration with email validation
- Secure password hashing (SHA-256)
- Password strength requirements (min 6 chars, uppercase, digit)
- SQLite database for user storage
- Modern GUI with tkinter
- Docker containerization for cross-platform deployment

## Quick Start

### Running with Docker Compose

```bash
docker-compose up --build
```

### Building and Running Manually

**Build the image:**
```bash
docker build -t login-app:latest .
```

**Run the container:**
```bash
docker run -it -v %cd%\users.db:/app/users.db login-app:latest
```

On Linux/macOS:
```bash
docker run -it -v $(pwd)/users.db:/app/users.db login-app:latest
```

## Usage

1. **Register**: Click "Create New Account" to register a new user
   - Username: any unique username
   - Email: valid email address
   - Password: minimum 6 characters, must include uppercase letter and digit

2. **Login**: Enter your credentials and click "Login"

3. **Dashboard**: Upon successful login, you'll see a welcome message

## Database

User credentials are stored in `users.db` (SQLite database). The database is persisted via Docker volumes.

## File Structure

- `app.py` - Main application code
- `Dockerfile` - Docker image definition
- `docker-compose.yml` - Docker Compose configuration
- `.dockerignore` - Files to exclude from Docker build
- `users.db` - SQLite database (created on first run)

## Requirements

- Docker
- Docker Compose (optional, for using docker-compose.yml)

## Password Requirements

- Minimum 6 characters
- At least one uppercase letter
- At least one digit

## Notes

- Passwords are hashed using SHA-256 before storage
- The application uses tkinter for GUI (built-in Python module)
- Database schema is automatically created on first run
