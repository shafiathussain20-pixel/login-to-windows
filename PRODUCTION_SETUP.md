# Production Setup Guide

## Environment Variables & Secrets Management

### 1. Generate a Strong Database Password

Use a secure password generator. Example on Linux/macOS:

```bash
# Generate a 32-character random password
openssl rand -base64 32

# Example output:
# Tr0pical!Flamingo#42$Secure@2024X7yZ9jK+lM=nO
```

Or use Python:

```python
import secrets
password = secrets.token_urlsafe(32)
print(password)
```

### 2. Create .env File for Local Development

Copy `.env.example` and fill in your values:

```bash
cp .env.example .env
```

Edit `.env`:

```env
DB_PASSWORD=your_secure_password_here
APP_DEBUG=false
LOG_LEVEL=INFO
```

**⚠️ NEVER commit `.env` to version control!**

### 3. Docker Environment Setup

#### Option A: Using .env file

```bash
# Linux/macOS
export $(cat .env | xargs)
docker run -it -v $(pwd)/users.db:/app/users.db -e DB_PASSWORD=$DB_PASSWORD login-app:latest

# Windows PowerShell
Get-Content .env | ForEach-Object {
    if ($_ -notmatch '^\s*#' -and $_ -notmatch '^\s*$') {
        $name, $value = $_.split('=')
        [Environment]::SetEnvironmentVariable($name, $value)
    }
}
docker run -it -v ${PWD}\users.db:/app/users.db -e DB_PASSWORD=$env:DB_PASSWORD login-app:latest
```

#### Option B: Using docker-compose with .env

```bash
docker compose up
```

The `.env` file is automatically loaded by docker-compose.

#### Option C: Manual environment variable

```bash
docker run -it \
  -v $(pwd)/users.db:/app/users.db \
  -e DB_PASSWORD="your_secure_password_here" \
  login-app:latest
```

### 4. Kubernetes Secrets

Create a secret for production Kubernetes deployment:

```bash
# Create a secret from literals
kubectl create secret generic login-app-secrets \
  --from-literal=DB_PASSWORD='your_secure_password_here'

# Or from file
kubectl create secret generic login-app-secrets \
  --from-file=db-password=.env
```

Use in deployment YAML:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: login-app
spec:
  template:
    spec:
      containers:
      - name: login-app
        image: your-registry/login-app:latest
        env:
        - name: DB_PASSWORD
          valueFrom:
            secretKeyRef:
              name: login-app-secrets
              key: DB_PASSWORD
        volumeMounts:
        - name: db
          mountPath: /app/users.db
```

### 5. GitHub Actions Secrets

Set up secrets for automated pushes to Docker Hub:

1. Go to your GitHub repository
2. Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Add the following secrets:

| Secret Name | Value |
|-------------|-------|
| `DOCKER_USERNAME` | Your Docker Hub username |
| `DOCKER_PASSWORD` | Your Docker Hub personal access token |

**Get Docker Hub Personal Access Token:**
1. Go to https://hub.docker.com/settings/security
2. Click "New Access Token"
3. Set permissions to "Read & Write"
4. Copy the token and paste it as `DOCKER_PASSWORD` secret

### 6. AWS Secrets Manager

Store secrets in AWS:

```bash
# Create secret
aws secretsmanager create-secret \
  --name login-app/db-password \
  --secret-string 'your_secure_password_here'

# Retrieve secret
aws secretsmanager get-secret-value \
  --secret-id login-app/db-password
```

Use in Docker or ECS:

```bash
# Fetch and run
SECRET=$(aws secretsmanager get-secret-value --secret-id login-app/db-password --query SecretString --output text)
docker run -e DB_PASSWORD="$SECRET" login-app:latest
```

### 7. HashiCorp Vault

For enterprise deployments:

```bash
# Authenticate
vault login

# Write secret
vault kv put secret/login-app db_password=your_secure_password_here

# Read secret
vault kv get secret/login-app
```

## Production Checklist

### Before Deployment

- [ ] Generate strong DB_PASSWORD (32+ characters, alphanumeric + symbols)
- [ ] Store password in secret management system (AWS Secrets Manager, Vault, etc.)
- [ ] Never commit `.env` file to git
- [ ] Verify `.gitignore` includes `.env` and secrets files
- [ ] Update `LOG_LEVEL` to `WARNING` or `ERROR` in production
- [ ] Set `APP_DEBUG=false`
- [ ] Use persistent volumes for database storage
- [ ] Enable database backups
- [ ] Set up monitoring and logging

### Security Hardening

1. **Network Security**
   ```yaml
   # Use network policies to restrict traffic
   kind: NetworkPolicy
   metadata:
     name: login-app-policy
   spec:
     podSelector:
       matchLabels:
         app: login-app
     policyTypes:
     - Ingress
     - Egress
   ```

2. **Container Security**
   ```dockerfile
   # Run as non-root user
   USER 1000:1000
   
   # Use read-only root filesystem
   RUN chmod -R 755 /app
   ```

3. **Resource Limits**
   ```yaml
   resources:
     limits:
       cpu: "500m"
       memory: "512Mi"
     requests:
       cpu: "250m"
       memory: "256Mi"
   ```

4. **Health Checks**
   ```yaml
   livenessProbe:
     exec:
       command:
       - python
       - -c
       - "import sqlite3; sqlite3.connect('/app/users.db')"
     initialDelaySeconds: 30
     periodSeconds: 10
   ```

### Database Backups

Automated backup script:

```bash
#!/bin/bash
# backup-db.sh

BACKUP_DIR="/backups/login-app"
DB_FILE="/app/users.db"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup with compression
cp $DB_FILE $BACKUP_DIR/users_${TIMESTAMP}.db
gzip $BACKUP_DIR/users_${TIMESTAMP}.db

# Keep only last 30 days of backups
find $BACKUP_DIR -name "*.gz" -mtime +30 -delete

echo "Database backed up: $BACKUP_DIR/users_${TIMESTAMP}.db.gz"
```

Schedule with cron:

```
# Backup every day at 2 AM
0 2 * * * /scripts/backup-db.sh
```

### Monitoring & Logging

Add structured logging:

```python
import logging
import json

logging.basicConfig(
    level=logging.INFO,
    format=json.dumps({
        "timestamp": "%(asctime)s",
        "level": "%(levelname)s",
        "message": "%(message)s"
    })
)

logger = logging.getLogger(__name__)
logger.info("User login attempt")
```

### Compliance

- **GDPR:** Ensure user data is encrypted and deletable
- **PCI-DSS:** If storing payment data, meet compliance standards
- **HIPAA:** If handling health data, implement required security controls
- **SOC 2:** Regular security audits and penetration testing

## Environment-Specific Configurations

### Development (.env.dev)
```env
DB_PASSWORD=dev_password_change_in_production
APP_DEBUG=true
LOG_LEVEL=DEBUG
```

### Staging (.env.staging)
```env
DB_PASSWORD=staging_strong_password_here
APP_DEBUG=false
LOG_LEVEL=INFO
```

### Production (.env.prod)
```env
DB_PASSWORD=production_very_strong_password_here
APP_DEBUG=false
LOG_LEVEL=WARNING
```

## Quick Reference Commands

```bash
# Generate secure password
openssl rand -base64 32

# Test environment variables locally
export DB_PASSWORD="test_password"
python app.py

# Run with docker-compose
docker-compose up -d

# View logs
docker-compose logs -f login-app

# Update image in production
docker-compose pull
docker-compose up -d

# Backup database
docker cp login-application:/app/users.db ./backup_users.db
```

## Support & Security Issues

- Report security vulnerabilities responsibly
- Keep dependencies updated
- Regular security audits recommended
- Monitor GitHub Actions workflow for deployment status
