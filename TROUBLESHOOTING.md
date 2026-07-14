# GitHub Actions CI/CD Troubleshooting Guide

## Issue Categories

- [Authentication Issues](#authentication-issues)
- [Test Failures](#test-failures)
- [Build Issues](#build-issues)
- [Deployment Issues](#deployment-issues)
- [Secret/Environment Issues](#secretenvironment-issues)
- [Performance Issues](#performance-issues)
- [Workflow Configuration Issues](#workflow-configuration-issues)

---

## Authentication Issues

### Issue: "Login failed" or "Invalid credentials"

**Symptoms:**
- Error in "Log in to Docker Hub" step
- Message: "Error response from daemon: login attempt failed"

**Common Causes:**
1. Wrong DOCKER_USERNAME
2. Invalid/expired DOCKER_PASSWORD token
3. Token doesn't have "Read & Write" permissions

**Solutions:**

**Solution 1: Verify Secret Names**
```bash
# Check GitHub secrets page
# Go to: Settings → Secrets and variables → Actions

# Should show:
# ✓ DOCKER_PASSWORD
# ✓ DOCKER_USERNAME

# NOT:
# ✗ DOCKER_USER
# ✗ DOCKER_TOKEN
# ✗ DOCKERHUB_USERNAME
```

**Solution 2: Verify Token Validity**
```bash
# Go to Docker Hub: https://hub.docker.com/settings/security
# Check if token still exists and hasn't expired
# If expired or missing, create new token:
# 1. Click "New Access Token"
# 2. Name: "github-actions"
# 3. Permissions: "Read & Write"
# 4. Click "Generate"
# 5. Copy token
# 6. Update DOCKER_PASSWORD secret in GitHub
```

**Solution 3: Verify Permissions**
```bash
# At Docker Hub, find your token
# Click the token name to see details
# Check: "Permissions" shows "Read & Write"

# If not:
# 1. Delete the token
# 2. Create new token with "Read & Write"
# 3. Update GitHub secret
```

**Solution 4: Username Not Email**
```bash
# DOCKER_USERNAME should be:
# ✓ Your Docker Hub username (e.g., "john-doe")
# ✓ NOT your email

# Find correct username:
# 1. Go to https://hub.docker.com/settings/profile
# 2. "Username" field shows your username
# 3. Update GitHub secret if different
```

### Issue: "401 Unauthorized" when pushing

**Symptoms:**
- Error in "Push to Docker Hub" step
- Message: "denied: requested access to the resource is denied"

**Solutions:**

```bash
# Step 1: Verify token is still valid
# Go to https://hub.docker.com/settings/security
# Check token is not expired

# Step 2: Generate new token if needed
# Go to https://hub.docker.com/settings/security
# Click "New Access Token"
# Select "Read & Write" permissions
# Copy the token

# Step 3: Update GitHub secret
# Go to https://github.com/YOUR-USERNAME/login-app/settings/secrets/actions
# Edit DOCKER_PASSWORD
# Paste new token
# Save

# Step 4: Retry workflow
# Go to Actions tab
# Click failed workflow
# Click "Re-run all jobs"
```

---

## Test Failures

### Issue: "ModuleNotFoundError: No module named 'pysqlcipher3'"

**Symptoms:**
- Test job fails during "Run unit tests" step
- Error during "Install dependencies"

**Solutions:**

```bash
# Solution 1: Verify requirements.txt is correct
cat requirements.txt

# Should contain:
# pysqlcipher3==1.2.0
# python-dotenv==1.0.0

# Solution 2: If missing, update requirements.txt
echo "pysqlcipher3==1.2.0" > requirements.txt
echo "python-dotenv==1.0.0" >> requirements.txt

# Solution 3: Commit and push
git add requirements.txt
git commit -m "Fix requirements.txt"
git push origin main

# Solution 4: Wait for workflow to complete
```

### Issue: "Test failed: tests error out"

**Symptoms:**
- Tests run but some fail
- Error messages in test output

**Solutions:**

```bash
# Step 1: Run tests locally
python -m unittest test_app -v

# Step 2: Fix any local failures
# Review error messages
# Make code changes

# Step 3: Run tests again
python -m unittest test_app -v

# Step 4: If all pass locally but fail in CI
# Check for environment variable issues
export DB_PASSWORD="test_password"
python -m unittest test_app -v

# Step 5: Verify Docker test works
docker run --rm -e DB_PASSWORD="test" login-app:latest \
  python -m unittest test_app -v

# Step 6: Fix any remaining issues
# Commit and push
git add .
git commit -m "Fix test failures"
git push origin main
```

### Issue: "Coverage report fails" or "Coverage command not found"

**Symptoms:**
- Test job completes but coverage report step fails
- Message: "command 'coverage' not found"

**Solutions:**

```bash
# This is usually not critical - tests still pass
# But to fix:

# Add coverage to requirements.txt
echo "coverage>=7.0" >> requirements.txt

# Commit and push
git add requirements.txt
git commit -m "Add coverage to requirements"
git push origin main
```

---

## Build Issues

### Issue: "Docker build fails" or "failed to solve"

**Symptoms:**
- Build job fails during Docker build step
- Error: "failed to solve: ..."

**Possible Causes & Solutions:**

**Solution 1: Base Image Not Found**
```bash
# Check Dockerfile first line
cat Dockerfile | head -1

# Should show:
# FROM python:3.11-slim

# If different, update it:
sed -i '1s/.*/FROM python:3.11-slim/' Dockerfile

git add Dockerfile
git commit -m "Fix base image"
git push origin main
```

**Solution 2: Disk Space Issue (Rare)**
```bash
# This is on GitHub's runner, usually not an issue
# If it persists, try clearing cache:

# In GitHub Actions, can't directly clear
# Workaround - force rebuild:
git commit --allow-empty -m "Rebuild - clear cache"
git push origin main
```

**Solution 3: Network Issue (Usually Temporary)**
```bash
# Wait a minute and retry
# Click "Re-run all jobs" in Actions tab

# Or force new commit:
git commit --allow-empty -m "Retry CI/CD"
git push origin main
```

### Issue: "Package installation fails during Docker build"

**Symptoms:**
- Build fails in "RUN pip install" step
- Message: "ERROR: Could not find a version that satisfies..."

**Solutions:**

```bash
# Check package version in requirements.txt
cat requirements.txt

# Verify all versions are available
# For pysqlcipher3 (common issue):
# Use version 1.2.0 - don't use 1.0.8 (doesn't exist)

# Fix requirements.txt:
echo "pysqlcipher3==1.2.0" > requirements.txt
echo "python-dotenv==1.0.0" >> requirements.txt

# Commit and push
git add requirements.txt
git commit -m "Fix package versions"
git push origin main

# Retry workflow
```

### Issue: "Image too large" or "Layer too large"

**Symptoms:**
- Build succeeds but takes very long
- Docker Hub upload slow

**Solutions:**

```bash
# This is usually OK - image is ~683MB
# To reduce size (advanced):

# 1. Update Dockerfile to remove build tools after build
# 2. Use multi-stage builds
# 3. Clean apt cache

# For now, this is acceptable
# Production performance is fine
```

---

## Deployment Issues

### Issue: "Push to Docker Hub fails" after build succeeds

**Symptoms:**
- Build job completes successfully
- But "Push to Docker Hub" step fails
- Error: "denied: requested access to the resource is denied"

**Solutions:**

```bash
# Step 1: Verify image was built
# Look for "Pushed" messages in build output

# Step 2: Check Docker Hub secret
# Verify DOCKER_PASSWORD is set (not empty)

# Step 3: Test token locally (if possible)
docker login -u YOUR-USERNAME -p YOUR-TOKEN

# Step 4: If that fails, get new token
# Go to https://hub.docker.com/settings/security
# Create new "Read & Write" token
# Update GitHub secret

# Step 5: Retry workflow
git commit --allow-empty -m "Retry push"
git push origin main
```

### Issue: "Image pushed but can't pull from Docker Hub"

**Symptoms:**
- Push succeeds (checkmark in workflow)
- But `docker pull` command fails
- Error: "image not found" or "Error response from daemon"

**Solutions:**

```bash
# Step 1: Wait a minute for Docker Hub to sync
sleep 60

# Step 2: Try pulling again
docker pull YOUR-USERNAME/login-app:latest

# Step 3: If still fails, check Docker Hub directly
# Go to https://hub.docker.com/r/YOUR-USERNAME/login-app
# Verify image is listed

# Step 4: Try pulling specific tag
docker pull YOUR-USERNAME/login-app:latest

# Step 5: If repository doesn't exist on Docker Hub
# This usually means push failed silently
# Check GitHub Actions logs more carefully
# Likely an authentication issue - see authentication section
```

### Issue: "Image pushed but production won't pull"

**Symptoms:**
- GitHub Actions shows successful push
- But production server can't pull
- Error: "Error response from daemon"

**Solutions:**

```bash
# Step 1: Verify authentication on production server
docker login -u YOUR-USERNAME -p YOUR-TOKEN

# Step 2: Check if token has expired
# Go to Docker Hub settings
# Create new token if needed

# Step 3: Update .env on production
export DOCKER_PASS="your-new-token"

# Step 4: Try pulling
docker pull YOUR-USERNAME/login-app:latest

# Step 5: If using Watchtower, restart it
docker restart watchtower
```

---

## Secret/Environment Issues

### Issue: "DB_PASSWORD not set" or "environment variable not found"

**Symptoms:**
- Container logs show warning about default password
- Application seems to use default DB_PASSWORD

**Solutions:**

**In GitHub Actions:**
```bash
# Step 1: Verify workflow has environment variables
cat .github/workflows/ci-cd.yml | grep -A5 "environment:"

# Step 2: Should show environment variables being passed
# If not in workflow file, add them

# Step 3: Commit and retry
git add .github/workflows/ci-cd.yml
git commit -m "Fix environment variables"
git push origin main
```

**In Production:**
```bash
# Step 1: Verify .env exists
ls -la .env

# Step 2: Verify .env has DB_PASSWORD
cat .env | grep DB_PASSWORD

# Step 3: If missing, add it
echo "DB_PASSWORD=your_strong_password" >> .env

# Step 4: Reload container
docker stop login-app-prod
docker rm login-app-prod

# Re-run container with updated .env
docker run -d \
  --name login-app-prod \
  -e DB_PASSWORD="$(cat .env | grep DB_PASSWORD | cut -d'=' -f2)" \
  YOUR-USERNAME/login-app:latest
```

### Issue: ".env file committed to git"

**Symptoms:**
- Warning: ".env appears in git history"
- Security concern: secrets exposed

**Solutions:**

```bash
# Step 1: Stop the leak
echo ".env" >> .gitignore

# Step 2: Remove from git (doesn't delete file locally)
git rm --cached .env

# Step 3: Commit the change
git commit -m "Remove .env from git tracking"

# Step 4: Push
git push origin main

# Step 5: IMPORTANT - Rotate credentials
# Go to Docker Hub settings
# Delete compromised token
# Create new token
# Update GitHub secret

# Step 6: Clean git history (advanced, if really needed)
# This requires force push - only if .env had real secrets
# Most of time, steps 1-5 are sufficient
```

---

## Performance Issues

### Issue: "Workflow takes too long"

**Symptoms:**
- Workflow runs for 10+ minutes
- Much slower than expected

**Common Causes:**

```bash
# 1. Test job slow
# Usually just python/pip setup first time
# Should be cached on next run

# 2. Build job slow
# First build is slow (no cache)
# Subsequent builds should use cache

# 3. Docker Hub push slow
# Depends on network
# Usually 1-2 MB/s

# Solution: Just wait, usually speeds up
# GitHub caches layers between runs
```

### Issue: "Workflow timeout" or "job cancelled after 360 minutes"

**Symptoms:**
- Workflow marked as cancelled
- "The operation was cancelled"

**Unlikely for this project** (our pipeline is ~3-5 minutes)

**But if it happens:**
```bash
# GitHub has 6-hour timeout on workflows
# Our pipeline shouldn't hit this
# If it does, likely stuck in build

# Solution:
# 1. Check last successful workflow
# 2. Compare to current
# 3. Look for what changed
# 4. Revert that change
# 5. Re-push

# Or restart workflow:
git commit --allow-empty -m "Retry - timeout"
git push origin main
```

---

## Workflow Configuration Issues

### Issue: "Workflow not running at all"

**Symptoms:**
- Push code but Actions tab stays empty
- No workflow appears

**Solutions:**

```bash
# Step 1: Check workflow file exists
ls -la .github/workflows/ci-cd.yml

# Step 2: Verify workflow file is valid YAML
# No tabs (only spaces)
# Proper indentation (2 spaces)

# Step 3: Check branch in workflow
grep "branches:" .github/workflows/ci-cd.yml

# Should show:
# branches: [ main, develop ]

# Make sure you're pushing to one of these branches

# Step 4: If pushing to different branch
# Either:
# A. Add branch to workflow file, OR
# B. Push to main or develop branch

# Example - add new branch to workflow:
sed -i 's/branches: \[ main, develop \]/branches: [ main, develop, feature-branch ]/' .github/workflows/ci-cd.yml

# Commit and push
git add .github/workflows/ci-cd.yml
git commit -m "Add feature branch to CI/CD"
git push origin feature-branch
```

### Issue: "Workflow fails with 'undefined variable' or 'syntax error'"

**Symptoms:**
- Workflow has red X
- Error in Actions logs about syntax

**Solutions:**

```bash
# Step 1: Check workflow YAML syntax
# Go to: https://www.yamllint.com/
# Paste contents of .github/workflows/ci-cd.yml

# Step 2: Fix any syntax errors
# Common issues:
# - Tabs instead of spaces
# - Missing colons
# - Wrong indentation

# Step 3: Example fix - wrong indentation
# Before (❌ WRONG):
# jobs:
#   test:
#     runs-on: ubuntu-latest
#      steps:  # Indented too much!

# After (✓ CORRECT):
# jobs:
#   test:
#     runs-on: ubuntu-latest
#     steps:  # Proper indentation

# Step 4: Commit and retry
git add .github/workflows/ci-cd.yml
git commit -m "Fix workflow syntax"
git push origin main
```

### Issue: "Secrets not available in workflow"

**Symptoms:**
- Workflow shows ${{ secrets.DOCKER_USERNAME }} literally
- Not substituted with actual value

**Solutions:**

```bash
# Step 1: Verify secrets are set
# Go to: Settings → Secrets and variables → Actions
# Should see:
# ✓ DOCKER_PASSWORD (hidden as ****)
# ✓ DOCKER_USERNAME (hidden as ****)

# Step 2: If secrets missing, add them
# Click "New repository secret"
# Add DOCKER_USERNAME and DOCKER_PASSWORD

# Step 3: Verify workflow references are correct
# In workflow file, should show:
# ${{ secrets.DOCKER_USERNAME }}
# ${{ secrets.DOCKER_PASSWORD }}

# NOT:
# ${{ DOCKER_USERNAME }}
# {{ secrets.DOCKER_USERNAME }}
# secrets.DOCKER_USERNAME

# Step 4: If wrong references, fix and commit
git add .github/workflows/ci-cd.yml
git commit -m "Fix secrets references"
git push origin main
```

---

## How to Get Help

### 1. Check Workflow Logs

```bash
# Go to GitHub Actions tab
# Click on failed workflow
# Click on failed job
# Scroll down to see detailed error logs
# Usually shows exactly what's wrong
```

### 2. Run Locally First

```bash
# Most CI/CD issues can be reproduced locally:

# Test locally
python -m unittest test_app -v

# Build Docker locally
docker build -t test:latest .

# Run Docker locally
docker run --rm -e DB_PASSWORD="test" test:latest python -m unittest test_app -v

# If all pass locally but fail in CI:
# Usually a secrets/environment issue
# Check GitHub Actions secrets
```

### 3. Use GitHub CLI

```bash
# Install: https://cli.github.com

# View workflows
gh run list --limit 10

# View specific run details
gh run view <RUN_ID>

# View run logs
gh run view <RUN_ID> --log

# Retry workflow
gh run rerun <RUN_ID>
```

### 4. Common Commands for Debugging

```bash
# Check secrets are accessible (they're masked in logs)
echo "DOCKER_USERNAME: ${{ secrets.DOCKER_USERNAME }}"
# Will show as: DOCKER_USERNAME: ****

# Debug workflow execution
# Add to workflow step:
- name: Debug
  run: |
    echo "Branch: ${{ github.ref }}"
    echo "Event: ${{ github.event_name }}"
    echo "Actor: ${{ github.actor }}"

# Check if secrets are set
- name: Check Secrets
  run: |
    if [ -z "${{ secrets.DOCKER_PASSWORD }}" ]; then
      echo "ERROR: DOCKER_PASSWORD not set"
      exit 1
    fi
```

---

## Quick Troubleshooting Checklist

When something fails:

- [ ] Check GitHub Actions logs for error message
- [ ] Run same operations locally to see if they work
- [ ] Verify GitHub secrets are set (Settings → Secrets)
- [ ] Verify requirements.txt has all dependencies
- [ ] Verify Dockerfile is valid
- [ ] Verify .github/workflows/ci-cd.yml is valid YAML
- [ ] Check if pushing to correct branch (main or develop)
- [ ] Verify Docker Hub credentials are correct
- [ ] Check if Docker Hub token expired
- [ ] Review recent changes that might have broken something

## Success Pattern

If you see this progression, everything is working:

```
✓ Test Job - 18/18 tests passing
✓ Security Scan - No issues
✓ Build Job - Image built and pushed
✓ Notify Job - All checks passed
```

Then:
```
✓ Image appears in Docker Hub
✓ docker pull succeeds
✓ Production container runs
✓ Database persists correctly
```

If you see this pattern, you're done! 🎉
