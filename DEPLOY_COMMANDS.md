# Step-by-Step Deploy Guide (Terminal Commands)

## Phase 1: Prepare (5 minutes)

### 1.1 Clone Your Repository

```bash
# If you haven't already
git clone https://github.com/YOUR-USERNAME/login-app.git
cd login-app

# Verify you're on the right branch
git branch -a
```

### 1.2 Verify All Files Are Present

```bash
# Check main application files
test -f app.py && echo "✓ app.py" || echo "✗ app.py"
test -f test_app.py && echo "✓ test_app.py" || echo "✗ test_app.py"
test -f requirements.txt && echo "✓ requirements.txt" || echo "✗ requirements.txt"
test -f Dockerfile && echo "✓ Dockerfile" || echo "✗ Dockerfile"
test -f docker-compose.yml && echo "✓ docker-compose.yml" || echo "✗ docker-compose.yml"

# Check configuration files
test -f .env.example && echo "✓ .env.example" || echo "✗ .env.example"
test -f .gitignore && echo "✓ .gitignore" || echo "✗ .gitignore"
test -f .dockerignore && echo "✓ .dockerignore" || echo "✗ .dockerignore"

# Check CI/CD
test -f .github/workflows/ci-cd.yml && echo "✓ .github/workflows/ci-cd.yml" || echo "✗ CI/CD missing"

# Check documentation
test -f README.md && echo "✓ README.md" || echo "✗ README.md"
test -f GITHUB_SECRETS_AND_DEPLOY.md && echo "✓ Setup guide" || echo "✗ Setup guide"
```

### 1.3 Create Local .env for Testing

```bash
# Create from template
cp .env.example .env

# Set a test password (you can use any strong password)
# Linux/macOS
echo "DB_PASSWORD=TestPassword123!" >> .env
echo "APP_DEBUG=false" >> .env
echo "LOG_LEVEL=INFO" >> .env

# Windows (PowerShell)
Add-Content -Path .env -Value "DB_PASSWORD=TestPassword123!"
Add-Content -Path .env -Value "APP_DEBUG=false"
Add-Content -Path .env -Value "LOG_LEVEL=INFO"

# View it
cat .env
```

### 1.4 Verify .env is Ignored

```bash
# Should show .env in .gitignore
grep -n "\.env" .gitignore

# If it shows: ".env" - you're good!
# If nothing, add it:
echo ".env" >> .gitignore
```

## Phase 2: Get GitHub Secrets (5 minutes)

### 2.1 Get Docker Hub Personal Access Token

```bash
# Copy this link and open in browser
echo "Go to: https://hub.docker.com/settings/security"
echo "Click: New Access Token"
echo "Name: github-actions"
echo "Permissions: Read & Write"
echo "Click: Generate"
echo ""
echo "COPY THE TOKEN - You won't see it again!"
echo "It looks like: dckr_pat_xxxxxxxxxxxxxxxxxxxxxxxx"
```

**Manual Steps:**
1. Go to https://hub.docker.com/settings/security
2. Click "New Access Token"
3. Enter name: `github-actions`
4. Set to "Read & Write"
5. Click "Generate"
6. Copy the token

### 2.2 Get Your Docker Hub Username

```bash
# Your Docker Hub username
echo "Your Docker Hub username:"
echo "From: https://hub.docker.com/settings/profile"
echo "Or from your repository URL: hub.docker.com/r/YOUR-USERNAME/login-app"
```

## Phase 3: Add GitHub Secrets (5 minutes)

### 3.1 Open GitHub Secrets Page

```bash
# Open this URL in browser (replace YOUR-USERNAME)
echo "https://github.com/YOUR-USERNAME/login-app/settings/secrets/actions"
```

**Manual Steps:**
1. Go to your repository on GitHub
2. Click "Settings" (top right)
3. Click "Secrets and variables" → "Actions" (left sidebar)

### 3.2 Add DOCKER_USERNAME Secret

**In GitHub UI:**
1. Click "New repository secret"
2. Name: `DOCKER_USERNAME`
3. Value: Your Docker Hub username (e.g., `john-doe`)
4. Click "Add secret"

### 3.3 Add DOCKER_PASSWORD Secret

**In GitHub UI:**
1. Click "New repository secret"
2. Name: `DOCKER_PASSWORD`
3. Value: Paste your Personal Access Token
   - Example: `dckr_pat_xxxxxxxxxxxxxxxxxxxxxxxx`
4. Click "Add secret"

### 3.4 Verify Secrets Are Set

After adding both, you should see:
```
DOCKER_PASSWORD     Updated X minutes ago
DOCKER_USERNAME     Updated X minutes ago
```

## Phase 4: Test Locally (5 minutes)

### 4.1 Install Dependencies

```bash
# Create virtual environment (optional but recommended)
python -m venv venv

# Activate virtual environment
# Linux/macOS
source venv/bin/activate

# Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 4.2 Run Tests

```bash
# Run all tests
python -m unittest test_app -v

# Expected output:
# Ran 18 tests in 0.XXXs
# OK
```

### 4.3 Test with Environment Variable

```bash
# Set DB_PASSWORD
export DB_PASSWORD="test_password_123"

# Run tests
python -m unittest test_app -v

# Should still get: OK
```

### 4.4 Test with Docker Locally

```bash
# Build image
docker build -t login-app:test .

# Run tests in Docker
docker run --rm -e DB_PASSWORD="test123" login-app:test python -m unittest test_app -v

# Should see: OK
```

## Phase 5: Commit and Push (5 minutes)

### 5.1 Check Git Status

```bash
# See what changed
git status

# Should NOT show .env
# Should show modified app.py, test_app.py, requirements.txt, etc.
```

### 5.2 Stage All Files

```bash
# Add all changes
git add .

# Or add specific files if you made other changes
git add app.py test_app.py requirements.txt
git add Dockerfile docker-compose.yml
git add .env.example .gitignore .dockerignore
git add .github/
git add *.md
git add push-to-registry.*
```

### 5.3 Verify Nothing Sensitive Added

```bash
# Show what will be committed
git diff --cached --name-only

# Verify output:
# ✓ .env.example (safe - example template)
# ✓ .github/workflows/ci-cd.yml (safe)
# ✓ *.md (safe - documentation)
# ✗ .env (should NOT appear)
# ✗ users.db (should NOT appear)
# ✗ __pycache__ (should NOT appear)
```

### 5.4 Commit Changes

```bash
# Commit with descriptive message
git commit -m "Production release: Add environment variables and GitHub Actions CI/CD

Features:
- Implement DB_PASSWORD from environment variables
- Add python-dotenv for .env file support
- Create complete GitHub Actions CI/CD pipeline
- Add Bandit and TruffleHog security scanning
- Add comprehensive production documentation
- Add Docker registry deployment scripts"

# Verify commit
git log --oneline -1
```

### 5.5 Push to GitHub

```bash
# Push to main branch (or your branch)
git push origin main

# You should see:
# Counting objects: XX
# Compressing objects: 100% (XX/XX)
# Writing objects: 100% (XX/XX)
# ...
# To github.com:YOUR-USERNAME/login-app.git
#    abc1234..def5678  main -> main

# Success! Now go to Actions tab
```

## Phase 6: Monitor Pipeline (5 minutes)

### 6.1 Open Actions Tab

```bash
# Open browser to your Actions page
echo "https://github.com/YOUR-USERNAME/login-app/actions"

# Or use GitHub CLI
gh run list --limit 10
```

### 6.2 Watch Workflow Execute

You should see a workflow with your commit message running:

```
Workflow Status: In Progress

Jobs:
  🟡 test - Running...
  🟡 security-scan - Running...
  ⏳ build - Waiting...
  ⏳ notify - Waiting...
```

### 6.3 Wait for Completion

Expected timeline:
- **Test Job:** ~30 seconds
- **Security Scan:** ~30 seconds
- **Build Job:** ~1-2 minutes
- **Notify:** ~10 seconds

Total time: **~3-5 minutes**

### 6.4 Check Final Status

```bash
# When complete, should show:
✓ test - Completed successfully
✓ security-scan - Completed successfully
✓ build - Completed successfully
✓ notify - Completed successfully
```

All green checkmarks = SUCCESS! 🎉

## Phase 7: Verify Deployment (5 minutes)

### 7.1 Check Docker Hub

```bash
# Go to Docker Hub
echo "https://hub.docker.com/r/YOUR-USERNAME/login-app"

# Should see:
# - Repository: login-app
# - Tags: latest, YOUR-COMMIT-SHA
# - Last updated: Just now
```

### 7.2 Pull Image Locally

```bash
# Login to Docker Hub
docker login
# Enter username and password when prompted

# Pull the image that was just pushed
docker pull YOUR-USERNAME/login-app:latest

# Should see download progress and end with:
# Status: Downloaded newer image for YOUR-USERNAME/login-app:latest
```

### 7.3 Test Pulled Image

```bash
# Run tests in pulled image
docker run --rm -e DB_PASSWORD="test123" YOUR-USERNAME/login-app:latest \
  python -m unittest test_app -v

# Should see:
# Ran 18 tests in 0.XXXs
# OK
```

### 7.4 Run Pulled Image

```bash
# Run the application
docker run -d \
  --name login-app-demo \
  -e DB_PASSWORD="DemoPassword123!" \
  -v $(pwd)/demo_users.db:/app/users.db \
  YOUR-USERNAME/login-app:latest

# Check it's running
docker ps | grep login-app-demo

# Check logs
docker logs login-app-demo

# Stop when done
docker stop login-app-demo
docker rm login-app-demo
```

## Phase 8: Deploy to Production (10 minutes)

### 8.1 Generate Strong Production Password

```bash
# Generate 32-character random password
# Linux/macOS
openssl rand -base64 32

# Windows PowerShell
[Convert]::ToBase64String((1..32 | ForEach-Object {[byte](Get-Random -Maximum 256)}))

# Copy the output, e.g.:
# K7mP9xQ2vL4zJ8cR5wN1bF3tH6sD0eAu2I9kL7mN3p0x
```

### 8.2 Create Production .env

```bash
# On production server
ssh your-server

# Create .env with production password
cat > .env << EOF
DB_PASSWORD=YOUR_GENERATED_PASSWORD_HERE
APP_DEBUG=false
LOG_LEVEL=WARNING
EOF

# Verify it
cat .env

# Lock it down (Linux/macOS only)
chmod 600 .env
```

### 8.3 Pull Production Image

```bash
# On production server
docker login

# Pull latest version
docker pull YOUR-USERNAME/login-app:latest

# Verify image
docker images YOUR-USERNAME/login-app
```

### 8.4 Run Production Container

```bash
# Create data directory
mkdir -p /data/login-app

# Run container
docker run -d \
  --name login-app-prod \
  --restart unless-stopped \
  -e DB_PASSWORD="$(cat .env | grep DB_PASSWORD | cut -d'=' -f2)" \
  -e APP_DEBUG=false \
  -e LOG_LEVEL=WARNING \
  -v /data/login-app/users.db:/app/users.db \
  YOUR-USERNAME/login-app:latest

# Check it's running
docker ps

# View logs
docker logs login-app-prod

# Check status
docker inspect login-app-prod | grep Status
```

### 8.5 Setup Auto-Updates (Optional)

```bash
# Use Watchtower to auto-update on new pushes
docker run -d \
  --name watchtower \
  --restart unless-stopped \
  -v /var/run/docker.sock:/var/run/docker.sock \
  containrrr/watchtower YOUR-USERNAME/login-app:latest

# Now every time you push new code:
# 1. CI/CD pipeline builds image
# 2. Image pushed to Docker Hub
# 3. Watchtower detects new image
# 4. Automatically pulls and restarts container
```

## Phase 9: Ongoing Maintenance

### 9.1 Making Updates

For any code changes:

```bash
# 1. Make changes locally
nano app.py

# 2. Test locally
python -m unittest test_app -v

# 3. Commit
git add .
git commit -m "Your change description"

# 4. Push
git push origin main

# 5. Monitor Actions tab
# 6. Wait for deployment
# 7. Production automatically updates (if using Watchtower)
```

### 9.2 Monitoring Deployments

```bash
# View all workflow runs
gh run list --limit 20

# View specific run
gh run view RUN_ID

# View run logs
gh run view RUN_ID --log

# Check production logs
docker logs login-app-prod --follow
```

### 9.3 Backup Production Database

```bash
# Backup production database
docker cp login-app-prod:/app/users.db ./backup_users_$(date +%Y%m%d_%H%M%S).db

# List backups
ls -lh backup_users_*.db

# Or automated daily backup
# Add to crontab:
# 0 2 * * * docker cp login-app-prod:/app/users.db /backups/users_$(date +\%Y\%m\%d).db
```

## Quick Reference Commands

```bash
# Git commands
git status                              # See what changed
git add .                              # Stage all files
git commit -m "message"                # Commit changes
git push origin main                   # Push to GitHub
git log --oneline                      # View commit history

# Test commands
python -m unittest test_app -v         # Run all tests
python -c "import app; print('✓')"    # Test import

# Docker commands
docker build -t login-app:test .       # Build locally
docker run --rm -e DB_PASSWORD=X Y     # Run test
docker pull YOUR-USERNAME/login-app    # Pull from Hub
docker ps                              # See running containers
docker logs CONTAINER                  # View container logs
docker stop CONTAINER                  # Stop container

# Verification
docker inspect APP                     # Show app details
docker exec APP python -m test         # Run tests in container
docker stats                           # Monitor resource usage
```

## Success Checklist

Before considering deployment complete, verify:

```bash
# ✓ GitHub push succeeded
git log --oneline | head -1

# ✓ All workflow jobs passed
# (Check GitHub Actions tab - all green)

# ✓ Docker image on Docker Hub
docker pull YOUR-USERNAME/login-app:latest

# ✓ Tests passing in production image
docker run --rm -e DB_PASSWORD=test YOUR-USERNAME/login-app:latest \
  python -m unittest test_app -v

# ✓ Production container running
docker ps | grep login-app-prod

# ✓ Database persisting
docker exec login-app-prod ls -la /app/users.db

# ✓ Environment variables set
docker exec login-app-prod python -c "import os; print(os.getenv('DB_PASSWORD')[:5])"
```

## Troubleshooting Quick Reference

```bash
# Workflow not starting
git push origin main                    # Try again
# Wait 30 seconds and refresh Actions tab

# Tests failing locally
pip install -r requirements.txt         # Reinstall deps
python -m unittest test_app -v          # Run again

# Can't login to Docker
docker logout                           # Clear login
docker login                            # Login again

# Image won't push
docker login                            # Re-login
# Check DOCKER_USERNAME and DOCKER_PASSWORD secrets

# Production container won't start
docker logs login-app-prod              # Check logs
docker inspect login-app-prod           # Check status
# Verify DB_PASSWORD environment variable is set

# Need to rollback
docker pull YOUR-USERNAME/login-app:COMMIT_SHA  # Pull old version
docker stop login-app-prod
docker rm login-app-prod
# Re-run container with old image
```

## Done! 🎉

You've successfully:
- ✓ Set up GitHub Actions secrets
- ✓ Committed and pushed code
- ✓ Triggered automated CI/CD pipeline
- ✓ Built Docker image automatically
- ✓ Pushed to Docker Hub automatically
- ✓ Deployed to production
- ✓ Verified everything working

Your application is now fully automated and production-ready!
