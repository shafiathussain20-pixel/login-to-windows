# GitHub Secrets Setup & First Deploy

## Overview

This guide walks you through setting up GitHub Actions secrets and triggering your first automated deployment.

## Prerequisites

- GitHub repository with this code
- Docker Hub account
- Docker Hub Personal Access Token (not your password)

## Step 1: Get Docker Hub Personal Access Token

### A. Go to Docker Hub Settings

1. Open https://hub.docker.com/settings/security
2. Log in if needed

### B. Create Personal Access Token

1. Click "New Access Token" button
2. Enter token name: `github-actions`
3. Set Access Permissions to "Read & Write"
4. Click "Generate"
5. **COPY THE TOKEN** (you won't see it again!)
   - Token format: `dckr_pat_xxxxxxxxxxxxxxxxxxxxxxxx`

### C. Save Token Temporarily

Keep the token handy - you'll need it in the next step.

**⚠️ SECURITY WARNING:**
- Never share this token
- Never commit it to git
- Never paste it in messages/screenshots
- Treat it like a password

## Step 2: Add GitHub Secrets

### A. Go to Your GitHub Repository

1. Navigate to your GitHub repository
2. Click "Settings" (top navigation)

### B. Add First Secret (DOCKER_USERNAME)

1. Click "Secrets and variables" in left sidebar
2. Click "Actions"
3. Click "New repository secret" (green button)
4. For the secret:
   - **Name:** `DOCKER_USERNAME`
   - **Value:** Your Docker Hub username (e.g., `john-doe`)
5. Click "Add secret"

### C. Add Second Secret (DOCKER_PASSWORD)

1. Click "New repository secret" again
2. For the secret:
   - **Name:** `DOCKER_PASSWORD`
   - **Value:** Paste your Personal Access Token
     - Example: `dckr_pat_xxxxxxxxxxxxxxxxxxxxxxxx`
3. Click "Add secret"

### D. Verify Secrets Added

You should now see both secrets listed:
- ✓ DOCKER_PASSWORD
- ✓ DOCKER_USERNAME

Secrets show as dots for security: `****`

## Step 3: Prepare Local Code

### A. Clone Repository (if not done)

```bash
git clone https://github.com/your-username/login-app.git
cd login-app
```

### B. Verify All Files Present

```bash
# Check core files
ls -la app.py test_app.py requirements.txt Dockerfile docker-compose.yml

# Check configuration files
ls -la .env.example .gitignore .dockerignore

# Check CI/CD
ls -la .github/workflows/ci-cd.yml

# Check documentation
ls -la *.md
```

### C. Create Local .env for Testing

```bash
# Create .env from template
cp .env.example .env

# Edit with a test password (Linux/macOS)
nano .env

# Or Windows
notepad .env
```

Update the file:
```env
DB_PASSWORD=TestPassword123!
APP_DEBUG=false
LOG_LEVEL=INFO
```

### D. Verify .env is Ignored

Check that `.env` is in `.gitignore`:

```bash
# Linux/macOS
grep "^\.env$" .gitignore

# Windows PowerShell
Select-String -Path .gitignore "^\.env$"
```

Should show: `.env`

## Step 4: Commit and Push Code

### A. Check Git Status

```bash
git status
```

You should see files ready to commit:
```
On branch main
Changes not staged for commit:
  modified:   app.py
  modified:   docker-compose.yml
  modified:   requirements.txt
  new file:   .env.example
  new file:   .gitignore
  new file:   .github/workflows/ci-cd.yml
  new file:   *.md files
```

**Important:** `.env` should NOT appear (it's in .gitignore)

### B. Add All Files

```bash
git add .
```

Or add specific files:

```bash
git add app.py test_app.py requirements.txt Dockerfile docker-compose.yml
git add .env.example .gitignore .dockerignore
git add .github/workflows/ci-cd.yml
git add *.md
git add push-to-registry.sh push-to-registry.bat
```

### C. Check What Will Be Committed

```bash
git status
```

Verify:
- ✓ .env is NOT in the list
- ✓ users.db is NOT in the list
- ✓ __pycache__ is NOT in the list

### D. Commit Changes

```bash
git commit -m "Add environment variables, secrets management, and GitHub Actions CI/CD

- Implement DB_PASSWORD from environment variables
- Add python-dotenv for .env file support
- Create GitHub Actions workflow for automated testing
- Add Bandit security scanning
- Add TruffleHog secret detection
- Include comprehensive production setup documentation
- Add automated push scripts for Docker registry deployment"
```

### E. Push to GitHub

```bash
# Push to main branch
git push origin main

# Or if using different branch
git push origin your-branch-name
```

You should see:
```
Counting objects: 50, done.
Delta compression using up to 8 threads.
Compressing objects: 100% (45/45), done.
Writing objects: 100% (50/50), 25.00 KiB | 2.50 MiB/s, done.
Total 50 (delta 25), reused 0 (delta 0)
...
To github.com:your-username/login-app.git
   abc123..def456  main -> main
```

## Step 5: Monitor CI/CD Pipeline

### A. Go to Actions Tab

1. Go to your repository on GitHub
2. Click "Actions" tab (top navigation)

### B. Watch Workflow Execution

You should see a new workflow running with your commit message.

Click on the workflow to see detailed status:

**Status Flow:**
1. 🟡 **Test Job** - Running
   - Checkout code
   - Setup Python
   - Install dependencies
   - Run 18 unit tests
   - Generate coverage report

2. 🟡 **Security Scan Job** - Running (parallel)
   - Bandit security scan
   - TruffleHog secret detection

3. 🟡 **Build Job** - Waiting for Test & Security
   - Build Docker image
   - Run tests in Docker
   - Push to Docker Hub

4. 🟡 **Notify Job** - Waiting for others
   - Check overall status

### C. Wait for Completion

The entire pipeline should take 3-5 minutes.

**Expected Outcomes:**

✓ **Success (Green checkmarks)**
```
✓ Test Job - OK (18/18 tests passed)
✓ Security Scan Job - OK (no issues)
✓ Build Job - OK (image pushed to Docker Hub)
✓ Notify Job - OK (all checks passed)
```

❌ **If Something Fails**
- Click on the failed job
- Scroll to see error messages
- Check troubleshooting section below

## Step 6: Verify Docker Image Pushed

### A. Check Docker Hub

1. Go to https://hub.docker.com
2. Log in
3. Click "Repositories"
4. Look for `login-app` repository
5. You should see tags:
   - `latest` (main branch)
   - A specific commit SHA tag

### B. Verify Image Locally

```bash
# Login to Docker Hub
docker login

# Pull the image you just pushed
docker pull your-username/login-app:latest

# Verify it works
docker run --rm -e DB_PASSWORD="test123!" your-username/login-app:latest python -m unittest test_app -v
```

### C. Check Image Details

```bash
# View image info
docker inspect your-username/login-app:latest

# View image size
docker images your-username/login-app
```

## Step 7: Verify in Production

### A. Create Production .env

On your production server:

```bash
# Create .env with strong password
cat > .env << EOF
DB_PASSWORD=$(openssl rand -base64 32)
APP_DEBUG=false
LOG_LEVEL=WARNING
EOF

# Verify it was created
cat .env
```

### B. Run Production Container

```bash
# Set environment variable
export $(cat .env | xargs)

# Run container
docker run -d \
  --name login-app-prod \
  -e DB_PASSWORD="$DB_PASSWORD" \
  -v /data/users.db:/app/users.db \
  your-username/login-app:latest

# Check logs
docker logs login-app-prod

# Verify running
docker ps | grep login-app-prod
```

### C. Test Application

```bash
# Check if container is running
docker inspect login-app-prod

# Test database connectivity
docker exec login-app-prod python -c "import sqlite3; print('✓ Database OK')"
```

## Troubleshooting

### Workflow Stuck or Not Starting

**Problem:** Workflow doesn't appear in Actions tab

**Solution:**
1. Refresh the page
2. Wait 30 seconds
3. Check branch is `main` (or configured branch)
4. Verify commit message doesn't have `[skip ci]`

### Test Job Failed

**Problem:** "ModuleNotFoundError: No module named 'pysqlcipher3'"

**Solution:**
```bash
# Verify requirements.txt has dependencies
cat requirements.txt

# Should show:
# pysqlcipher3==1.2.0
# python-dotenv==1.0.0

# If missing, add them and push again
```

### Security Scan Failed

**Problem:** TruffleHog detected secrets

**Solution:**
1. Check what was detected: Click on failed job, scroll down
2. If it's a real secret (unlikely):
   - Rotate credentials immediately
   - Delete from git history
3. If it's a false positive:
   - It's usually fine to ignore
   - Workflow will still complete

### Build Job Failed - Docker Login Error

**Problem:** "Error response from daemon: login attempt to https://registry-1.docker.io failed"

**Solution:**
1. Verify `DOCKER_USERNAME` secret is set correctly
2. Verify `DOCKER_PASSWORD` secret is set correctly (not regular password)
3. Verify token has "Read & Write" permissions
4. Check if token expired (reset if needed)
5. Verify username is not an email

### Build Job Failed - Image Push Error

**Problem:** "Error: denied: requested access to the resource is denied"

**Solution:**
1. Your account may not have permission to push
2. Token might be invalid
3. Go to Docker Hub, generate new token, update secret:
   - Go to GitHub repo → Settings → Secrets
   - Edit `DOCKER_PASSWORD`
   - Paste new token
   - Retry by pushing empty commit: `git commit --allow-empty -m "Retry CI/CD" && git push`

### Need to Retry Pipeline

**Option 1: Push Empty Commit**
```bash
git commit --allow-empty -m "Retry CI/CD"
git push origin main
```

**Option 2: Re-run from GitHub UI**
1. Go to Actions tab
2. Click on the workflow
3. Click "Re-run all jobs"

**Option 3: Make a Code Change**
```bash
# Make any change (e.g., update README)
echo "# Updated at $(date)" >> README.md

# Commit and push
git add README.md
git commit -m "Update documentation"
git push origin main
```

## Common Mistakes & How to Avoid

### ❌ Mistake 1: Using Docker Hub Password Instead of Token

**Wrong:**
```
DOCKER_PASSWORD = "my_docker_hub_password"
```

**Correct:**
```
DOCKER_PASSWORD = "dckr_pat_xxxxxxxxxxxxxxxxxxxxxxxx"
```

**Fix:** Generate new Personal Access Token (Settings → Security)

### ❌ Mistake 2: Committing .env File

**Problem:** Secret DB_PASSWORD exposed in git history

**Fix:**
1. Never commit .env
2. Verify .gitignore contains `.env`
3. If already committed:
   ```bash
   git rm --cached .env
   git commit -m "Remove .env from tracking"
   git push
   ```

### ❌ Mistake 3: Setting Wrong Branch in Workflow

**Problem:** Workflow doesn't run on your branch

**Fix:** Check `.github/workflows/ci-cd.yml`
```yaml
on:
  push:
    branches: [ main, develop ]  # Make sure your branch is listed
```

### ❌ Mistake 4: Using Email Instead of Username

**Problem:** "invalid account" error

**Fix:**
- DOCKER_USERNAME should be your Docker Hub username (not email)
- If unsure, check: https://hub.docker.com/settings/profile

## Post-Deployment Checklist

After successful deployment:

- [ ] GitHub Actions workflow completed successfully
- [ ] Image pushed to Docker Hub
- [ ] Image tags are `latest` and commit SHA
- [ ] Can pull image: `docker pull your-username/login-app:latest`
- [ ] Tests passed in CI/CD
- [ ] Security scans passed
- [ ] No secrets detected in code
- [ ] Production container running
- [ ] Database persisting correctly

## Monitoring Deployments

### View Workflow History

```bash
# Show last 5 workflow runs
gh run list --limit 5

# Show specific workflow details
gh run view <run-id>

# Show workflow logs
gh run view <run-id> --log
```

(Requires GitHub CLI: https://cli.github.com)

### Browser Monitoring

1. Go to Actions tab regularly
2. Check recent workflow runs
3. Review logs if failures occur

### Email Notifications

1. GitHub can email on workflow failures
2. Go to Settings → Notifications
3. Configure "CI/CD" notifications

## Next Steps

### For Continued Development

1. Make code changes locally
2. Test: `python -m unittest test_app -v`
3. Commit: `git commit -m "Your changes"`
4. Push: `git push origin main`
5. Monitor workflow in Actions tab
6. Pull from Docker Hub when ready

### For Production Updates

1. Make code changes
2. Push to main branch
3. Wait for CI/CD to complete
4. Pull latest image: `docker pull your-username/login-app:latest`
5. Restart container: `docker-compose pull && docker-compose up -d`

### For Emergency Fixes

1. Make critical fix
2. Push to main
3. Manual pull if can't wait for CI/CD:
   ```bash
   docker pull your-username/login-app:latest
   docker-compose down
   docker-compose up -d
   ```

## Support Commands

```bash
# View workflow file
cat .github/workflows/ci-cd.yml

# Test locally before pushing
python -m unittest test_app -v

# Build Docker image locally
docker build -t test-image:latest .

# Test Docker image
docker run --rm test-image:latest python -m unittest test_app -v

# View Docker Hub repo
docker search your-username/login-app

# Pull specific tag
docker pull your-username/login-app:latest
docker pull your-username/login-app:main

# View image layers
docker history your-username/login-app:latest

# Get Docker Hub token
# Go to: https://hub.docker.com/settings/security
```

## Summary

You've successfully:

1. ✓ Created Docker Hub Personal Access Token
2. ✓ Added GitHub Actions secrets
3. ✓ Committed and pushed code
4. ✓ Triggered CI/CD pipeline
5. ✓ Built and pushed Docker image
6. ✓ Verified in production

Your login application is now:
- **Automated** - Tests run on every push
- **Secure** - Environment variables, no hardcoded secrets
- **Deployed** - Docker image on Docker Hub
- **Monitored** - GitHub Actions shows all runs
- **Production-ready** - Can be deployed anywhere Docker runs

🎉 **You're done! Your application is production-ready and fully automated.**
