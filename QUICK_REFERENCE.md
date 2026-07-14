# Quick Reference: Environment Variables & CI/CD

## Local Development

### 1. Create .env file
```bash
cp .env.example .env
```

### 2. Edit .env
```env
DB_PASSWORD=your_secure_password_here
APP_DEBUG=false
LOG_LEVEL=INFO
```

### 3. Run with docker-compose
```bash
docker compose up
```

### 4. Run tests
```bash
python -m unittest test_app -v
```

## Production Setup

### Generate strong password
```bash
# Linux/macOS
openssl rand -base64 32

# Windows PowerShell
[System.Convert]::ToBase64String((1..32 | ForEach-Object { [byte](Get-Random -Maximum 256) }))
```

### Set environment variable
```bash
# Linux/macOS
export DB_PASSWORD="your_secure_password_here"

# Windows PowerShell
$env:DB_PASSWORD="your_secure_password_here"

# Windows Command Prompt
set DB_PASSWORD=your_secure_password_here
```

### Run container with environment
```bash
docker run -e DB_PASSWORD="your_password" -v $(pwd)/users.db:/app/users.db login-app:latest
```

## GitHub Actions Setup

### 1. Create Docker Hub Personal Access Token
- Go to https://hub.docker.com/settings/security
- Click "New Access Token"
- Copy the token

### 2. Add GitHub Secrets
- Go to your repo → Settings → Secrets and variables → Actions
- Add secret: `DOCKER_USERNAME` = your Docker Hub username
- Add secret: `DOCKER_PASSWORD` = your token

### 3. Push code to trigger pipeline
```bash
git push origin main
```

### 4. Monitor in Actions tab
- Click "Actions" in your GitHub repo
- Watch pipeline run: Test → Security Scan → Build → Notify

## Testing

### Run tests locally
```bash
python -m unittest test_app -v
```

### Run tests in Docker
```bash
docker run --rm -e DB_PASSWORD="test" login-app:latest python -m unittest test_app -v
```

### Check test coverage
```bash
pip install coverage
coverage run -m unittest test_app
coverage report
```

## Security Checks

### Bandit (code security)
```bash
pip install bandit
bandit -r . -ll
```

### TruffleHog (secret detection)
```bash
pip install truffleHog
trufflehog filesystem . --json
```

## Deployment

### Push to Docker Hub
```bash
docker login
docker tag login-app:latest your-username/login-app:latest
docker push your-username/login-app:latest
```

### Pull and run from Docker Hub
```bash
docker pull your-username/login-app:latest
docker run -e DB_PASSWORD="your_password" your-username/login-app:latest
```

## Environment Variables

| Variable | Required | Default | Notes |
|----------|----------|---------|-------|
| `DB_PASSWORD` | Yes | dev_password_change_in_production | Should be 32+ chars |
| `APP_DEBUG` | No | false | Set to `true` only for development |
| `LOG_LEVEL` | No | INFO | Options: DEBUG, INFO, WARNING, ERROR |

## Security Checklist

- [ ] Generated strong DB_PASSWORD (32+ characters)
- [ ] Added secrets to GitHub Actions
- [ ] Never committed `.env` to git
- [ ] Updated `.gitignore` to exclude secrets
- [ ] Reviewed GitHub Actions workflow
- [ ] Set `APP_DEBUG=false` in production
- [ ] Configured database backups
- [ ] Enabled branch protection rules
- [ ] Required status checks to pass before merge

## Troubleshooting

**Docker build fails locally**
```bash
docker build --no-cache -t login-app:latest .
```

**Tests fail with permission error**
```bash
# Grant permissions
chmod +x .github/workflows/ci-cd.yml
```

**GitHub Actions won't push to Docker Hub**
1. Verify secrets are set correctly
2. Check token hasn't expired
3. Verify token has "Read & Write" permissions
4. Check username is correct (not email)

**Database file not persisting**
```bash
# Ensure volume is mounted correctly
docker run -v $(pwd)/users.db:/app/users.db login-app:latest
```

**Can't connect to database**
```bash
# Check DB_PASSWORD is set
docker run -e DB_PASSWORD="your_password" login-app:latest
```

## File References

- `.env.example` - Template for environment variables
- `.env` - Local environment (DO NOT COMMIT)
- `.gitignore` - Files to exclude from git
- `.github/workflows/ci-cd.yml` - GitHub Actions workflow
- `PRODUCTION_SETUP.md` - Detailed production guide
- `GITHUB_ACTIONS_SETUP.md` - GitHub Actions guide

## Useful Commands

```bash
# Generate env from template
cp .env.example .env

# Run with custom password
docker run -e DB_PASSWORD="MyPassword123!" login-app:latest

# View all container environment variables
docker inspect login-app-container | grep -A 20 "Env"

# Test environment variable in Python
docker run -e DB_PASSWORD="test" login-app:latest python -c "import os; print(os.getenv('DB_PASSWORD'))"

# Build without cache
docker build --no-cache -t login-app:latest .

# Push to multiple tags
docker tag login-app:latest username/login-app:v1.0.0
docker tag login-app:latest username/login-app:latest
docker push username/login-app:v1.0.0
docker push username/login-app:latest
```
