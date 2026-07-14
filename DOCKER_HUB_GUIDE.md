# Docker Hub Deployment Guide

## Prerequisites

- Docker installed and running
- Docker Hub account (create at https://hub.docker.com)

## Push to Docker Hub

### Step 1: Build the Image

```bash
docker build -t login-app:latest .
```

### Step 2: Login to Docker Hub

```bash
docker login
```

Enter your Docker Hub username and password when prompted.

### Step 3: Tag Your Image

Replace `your-username` with your Docker Hub username:

```bash
docker tag login-app:latest your-username/login-app:latest
docker tag login-app:latest your-username/login-app:v1.0.0
```

### Step 4: Push to Docker Hub

```bash
docker push your-username/login-app:latest
docker push your-username/login-app:v1.0.0
```

### Using the Push Scripts

Alternatively, use the provided scripts:

**On Linux/macOS:**
```bash
chmod +x push-to-registry.sh
./push-to-registry.sh docker.io your-username
```

**On Windows (PowerShell):**
```bash
./push-to-registry.bat your-username
```

## Pull from Docker Hub

After pushing, anyone can pull your image:

```bash
docker pull your-username/login-app:latest
```

## Run the Pulled Image

```bash
docker run -it -v %cd%\users.db:/app/users.db your-username/login-app:latest
```

Or with docker-compose:

```yaml
version: '3.8'

services:
  login-app:
    image: your-username/login-app:latest
    container_name: login-application
    volumes:
      - ./users.db:/app/users.db
    networks:
      - app-network

networks:
  app-network:
    driver: bridge
```

## Push to Other Registries

### GitHub Container Registry (ghcr.io)

```bash
docker login ghcr.io
docker tag login-app:latest ghcr.io/your-username/login-app:latest
docker push ghcr.io/your-username/login-app:latest
```

### Amazon ECR

```bash
aws ecr create-repository --repository-name login-app --region us-east-1
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789.dkr.ecr.us-east-1.amazonaws.com
docker tag login-app:latest 123456789.dkr.ecr.us-east-1.amazonaws.com/login-app:latest
docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/login-app:latest
```

### Google Container Registry (gcr.io)

```bash
gcloud auth configure-docker
docker tag login-app:latest gcr.io/your-project/login-app:latest
docker push gcr.io/your-project/login-app:latest
```

## Image Details

- **Image Name:** login-app
- **Base Image:** python:3.11-slim
- **Size:** ~900MB (with build tools)
- **Runtime Size:** ~600MB
- **Database:** SQLite with SQLCipher encryption
- **Tests:** 18 unit tests, all passing

## Security Notes

- Database is encrypted with SQLCipher (AES-256)
- Passwords are hashed with SHA-256
- Change `DB_PASSWORD` in app.py for production use
- Database file should be kept in a secure volume
- Consider using environment variables for sensitive configuration

## Version Management

Tag your images with semantic versioning:

```bash
docker tag login-app:latest your-username/login-app:v1.0.0
docker tag login-app:latest your-username/login-app:v1.0
docker tag login-app:latest your-username/login-app:latest

docker push your-username/login-app:v1.0.0
docker push your-username/login-app:v1.0
docker push your-username/login-app:latest
```

This allows users to:
- Pull specific versions: `docker pull your-username/login-app:v1.0.0`
- Pull latest stable: `docker pull your-username/login-app:v1.0`
- Pull latest: `docker pull your-username/login-app:latest`
