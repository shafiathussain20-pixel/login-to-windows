# Complete Deployment Checklist

## Pre-Deployment (15 minutes)

### Preparation
- [ ] Repository cloned locally: `git clone https://github.com/YOUR-USERNAME/login-app.git`
- [ ] All files present (verify with: `ls -la app.py test_app.py requirements.txt .github/workflows/ci-cd.yml`)
- [ ] .env created from .env.example: `cp .env.example .env`
- [ ] .gitignore contains `.env` (verify: `grep "^\.env$" .gitignore`)

### Dependencies & Testing
- [ ] Python 3.11+ installed: `python --version`
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] All 18 tests pass locally: `python -m unittest test_app -v`
- [ ] Docker installed: `docker --version`
- [ ] Docker running: `docker ps`
- [ ] Docker image builds: `docker build -t login-app:test .`
- [ ] Tests pass in Docker: `docker run --rm -e DB_PASSWORD="test" login-app:test python -m unittest test_app -v`

### Docker Hub Setup
- [ ] Docker Hub account active: https://hub.docker.com
- [ ] Logged in: `docker login`
- [ ] Personal Access Token generated: https://hub.docker.com/settings/security
- [ ] Token saved safely (will need in next step)
- [ ] Docker Hub username confirmed: `docker info | grep Username`

### Repository Setup
- [ ] Repository created on GitHub: https://github.com/new
- [ ] Code pushed to GitHub: `git push origin main`
- [ ] Branch exists on GitHub: Verify via web UI

---

## GitHub Actions Setup (5 minutes)

### Add DOCKER_USERNAME Secret
- [ ] Navigate to: GitHub repo → Settings → Secrets and variables → Actions
- [ ] Click "New repository secret"
- [ ] Name: `DOCKER_USERNAME`
- [ ] Value: Your Docker Hub username
- [ ] Click "Add secret"
- [ ] Verify it appears in list (shows as dots)

### Add DOCKER_PASSWORD Secret
- [ ] Click "New repository secret" again
- [ ] Name: `DOCKER_PASSWORD`
- [ ] Value: Your Docker Hub Personal Access Token (NOT password)
- [ ] Click "Add secret"
- [ ] Verify both secrets now showing

### Verify Secrets
- [ ] Both secrets visible: `DOCKER_PASSWORD` and `DOCKER_USERNAME`
- [ ] Neither secret shows actual value (all masked)
- [ ] Secrets updated timestamp shows recent

---

## Code Preparation (5 minutes)

### File Verification
- [ ] app.py updated with environment variable support
- [ ] test_app.py has 18 tests
- [ ] requirements.txt includes pysqlcipher3 and python-dotenv
- [ ] Dockerfile includes SQLCipher build dependencies
- [ ] docker-compose.yml references environment variables
- [ ] .github/workflows/ci-cd.yml exists and is valid

### Git Status Check
```bash
git status
```
- [ ] Only modified/new application files shown
- [ ] `.env` does NOT appear in the list
- [ ] `users.db` does NOT appear in the list
- [ ] `__pycache__` does NOT appear in the list

### Commit and Push
- [ ] Code staged: `git add .`
- [ ] Changes committed: `git commit -m "your-message"`
- [ ] Commit shows in log: `git log --oneline | head -1`
- [ ] Code pushed to main: `git push origin main`
- [ ] Push confirmed in terminal output

---

## CI/CD Pipeline Monitoring (5-10 minutes)

### Workflow Triggering
- [ ] Go to GitHub repository → Actions tab
- [ ] New workflow appears with your commit message
- [ ] Workflow status shows "In Progress"

### Test Job
- [ ] Test job started
- [ ] Checkout step completed
- [ ] Python setup completed
- [ ] Dependencies installed
- [ ] 18 tests ran successfully
- [ ] Coverage report generated
- [ ] Test job shows green checkmark ✓

### Security Scan Job
- [ ] Security scan started (usually parallel with Test)
- [ ] Bandit scan completed
- [ ] TruffleHog scan completed
- [ ] No critical issues detected
- [ ] Security job shows green checkmark ✓

### Build Job
- [ ] Build job started (after Test and Security pass)
- [ ] Docker Buildx setup completed
- [ ] Docker Hub login successful
- [ ] Docker image built successfully
- [ ] Tests run in Docker container pass
- [ ] Image pushed to Docker Hub
- [ ] Build job shows green checkmark ✓

### Notification Job
- [ ] Notify job started (after Build)
- [ ] Status check passed
- [ ] Notify job shows green checkmark ✓

### Overall Status
- [ ] All jobs completed: ~3-5 minutes total
- [ ] All jobs show green checkmarks ✓✓✓✓
- [ ] No job shows red X or yellow warning

---

## Docker Hub Verification (5 minutes)

### Repository Check
- [ ] Go to https://hub.docker.com/r/YOUR-USERNAME/login-app
- [ ] Repository exists
- [ ] Visibility is correct (Public/Private as intended)
- [ ] Description shows (if added)

### Image Tags
- [ ] `latest` tag exists and shows recent timestamp
- [ ] Commit SHA tag exists (long hash)
- [ ] Both tags point to same digest
- [ ] Image size shows (should be ~170MB)

### Image Details
- [ ] Click on latest tag
- [ ] Shows image was pushed successfully
- [ ] Creation timestamp is recent (just now)
- [ ] No pull errors shown

---

## Local Verification (5 minutes)

### Docker Pull
```bash
docker pull YOUR-USERNAME/login-app:latest
```
- [ ] Pull succeeds without errors
- [ ] Image downloads (shows progress)
- [ ] Completes with: "Status: Downloaded newer image"

### Test in Pulled Image
```bash
docker run --rm -e DB_PASSWORD="test123" YOUR-USERNAME/login-app:latest python -m unittest test_app -v
```
- [ ] Container starts
- [ ] All 18 tests pass
- [ ] Shows: "Ran 18 tests in 0.XXXs"
- [ ] Shows: "OK"

### Image Inspection
```bash
docker inspect YOUR-USERNAME/login-app:latest
```
- [ ] Image has all environment variables configured
- [ ] Image size is reasonable (~683MB on disk)
- [ ] Layers include SQLCipher and Python dependencies

---

## Production Setup (10 minutes)

### Production Server Preparation
- [ ] Server has Docker installed: `docker --version`
- [ ] Server has Docker running: `docker ps`
- [ ] Server has SSH access verified
- [ ] Backups configured (if needed)
- [ ] Monitoring setup (if needed)

### Production Database Setup
- [ ] Create data directory: `mkdir -p /data/login-app`
- [ ] Set permissions: `chmod 700 /data/login-app`
- [ ] Create production .env
- [ ] Generated strong DB_PASSWORD: `openssl rand -base64 32`
- [ ] Set DB_PASSWORD in production .env
- [ ] Locked down .env: `chmod 600 .env`

### Production Container Pull
```bash
docker login
docker pull YOUR-USERNAME/login-app:latest
```
- [ ] Login succeeds
- [ ] Pull succeeds
- [ ] Image available locally: `docker images YOUR-USERNAME/login-app`

### Production Container Run
```bash
docker run -d --name login-app-prod \
  --restart unless-stopped \
  -e DB_PASSWORD="$(cat .env | grep DB_PASSWORD | cut -d'=' -f2)" \
  -e APP_DEBUG=false \
  -e LOG_LEVEL=WARNING \
  -v /data/login-app/users.db:/app/users.db \
  YOUR-USERNAME/login-app:latest
```
- [ ] Container starts successfully
- [ ] No error messages in console
- [ ] Container shows in `docker ps`
- [ ] Container has status "Up"

### Production Container Verification
```bash
docker logs login-app-prod
docker ps | grep login-app-prod
docker inspect login-app-prod
```
- [ ] Logs show no errors
- [ ] Container appears in ps output
- [ ] Container inspect shows all environment variables
- [ ] Status shows "running"

### Production Health Check
```bash
docker exec login-app-prod python -c "import app; print('✓')"
```
- [ ] Command executes without error
- [ ] Shows checkmark
- [ ] Verifies application imports successfully

### Production Database Check
```bash
docker exec login-app-prod ls -la /app/users.db
```
- [ ] Database file exists
- [ ] File shows with size (or empty if first run)
- [ ] Permissions are correct

---

## Advanced: Watchtower Setup (Optional)

### Why Watchtower?
- Automatically pulls new images from Docker Hub
- Stops old container, starts new one
- Zero-downtime deployments

### Install Watchtower
```bash
docker run -d \
  --name watchtower \
  --restart unless-stopped \
  -v /var/run/docker.sock:/var/run/docker.sock \
  containrrr/watchtower YOUR-USERNAME/login-app:latest
```
- [ ] Watchtower starts successfully
- [ ] Shows in `docker ps`
- [ ] Container healthy

### Verify Watchtower Works
- [ ] Make small code change
- [ ] Commit and push: `git push origin main`
- [ ] Wait for CI/CD pipeline to complete (~5 minutes)
- [ ] Check Watchtower logs: `docker logs watchtower`
- [ ] Verify new image pulled and container restarted

---

## Backup & Recovery Setup

### Backup Strategy
- [ ] Backup location decided (local, cloud, etc.)
- [ ] Backup schedule determined (daily, weekly, etc.)
- [ ] Backup tested to restore

### Create Initial Backup
```bash
docker cp login-app-prod:/app/users.db ./backup_users_initial.db
```
- [ ] Backup command succeeds
- [ ] Backup file created: `ls -la backup_users_initial.db`

### Automated Daily Backup (Linux/macOS)
```bash
# Add to crontab: crontab -e
0 2 * * * docker cp login-app-prod:/app/users.db /backups/users_$(date +\%Y\%m\%d).db
```
- [ ] Crontab entry added
- [ ] Backup directory exists: `mkdir -p /backups`
- [ ] Proper permissions: `chmod 755 /backups`

---

## Monitoring & Logging Setup

### Container Logs
```bash
docker logs login-app-prod --follow
```
- [ ] Logs display without error
- [ ] No critical errors shown
- [ ] Can follow logs with --follow flag

### Container Stats
```bash
docker stats login-app-prod --no-stream
```
- [ ] Shows CPU usage (should be low when idle)
- [ ] Shows memory usage (should be <100MB)
- [ ] Shows network I/O

### Health Monitoring (Optional)
- [ ] Set up external monitoring (Datadog, New Relic, etc.) if needed
- [ ] Configure alerts for high CPU/memory
- [ ] Configure alerts for container crash
- [ ] Configure alerts for database issues

---

## Rollback Plan

### Know How to Rollback
- [ ] Previous image tag known (example: `your-username/login-app:commit-abc123`)
- [ ] Rollback procedure documented:
  1. Stop current container: `docker stop login-app-prod`
  2. Remove container: `docker rm login-app-prod`
  3. Pull old image: `docker pull your-username/login-app:OLDTAG`
  4. Restart with old image: `docker run -d ... your-username/login-app:OLDTAG`
- [ ] Database backup can restore if needed
- [ ] Team knows rollback procedure

---

## Update & Maintenance Schedule

### Regular Updates
- [ ] When to check for updates: (e.g., weekly)
- [ ] Update process: Push code → Wait for CI/CD → Watchtower auto-updates
- [ ] Notification when new version deployed
- [ ] Test new version doesn't break anything

### Dependency Updates
- [ ] Python 3.11 support verified
- [ ] SQLCipher latest version noted
- [ ] python-dotenv latest version noted
- [ ] Plan for when to update dependencies

---

## Final Sign-Off Checklist

### All Systems Go ✓
- [ ] Code pushed to GitHub
- [ ] GitHub Actions workflow complete (all green)
- [ ] Docker image on Docker Hub
- [ ] Production container running
- [ ] Database persisting correctly
- [ ] Can pull from Docker Hub
- [ ] Tests passing in production image
- [ ] Logs show no critical errors
- [ ] Backup strategy in place
- [ ] Monitoring configured
- [ ] Team trained on rollback

### Success Criteria Met
- [ ] User registration works
- [ ] User login works
- [ ] Database encryption active
- [ ] Environment variables configured
- [ ] CI/CD pipeline automated
- [ ] Security scans passing
- [ ] Container health verified

### Ready for Production ✓
- [ ] Application is secure
- [ ] Application is automated
- [ ] Application is monitored
- [ ] Application is backed up
- [ ] Team is trained
- [ ] Documentation is complete

---

## Post-Deployment Tasks

### Week 1
- [ ] Monitor application performance
- [ ] Check logs for any errors
- [ ] Verify backups running
- [ ] Get user feedback
- [ ] Test recovery from backup

### Month 1
- [ ] Review security scan results
- [ ] Check Docker Hub for new image tags
- [ ] Verify Watchtower is updating correctly
- [ ] Review performance metrics
- [ ] Document any issues encountered

### Ongoing
- [ ] Monitor CI/CD pipeline status
- [ ] Keep dependencies updated
- [ ] Review security advisories
- [ ] Maintain backup integrity
- [ ] Monitor application performance

---

## Documentation Sign-Off

After completing all items above:

```
Deployment Date: ________________
Deployed By: ____________________
Reviewed By: ____________________
Approved By: ____________________

Production URL: __________________
Admin Contact: ___________________
Backup Location: _________________
Monitoring Dashboard: ____________

All items verified: ✓ YES / __ NO

Notes:
________________________________________
________________________________________
________________________________________
```

---

## Success! 🎉

Your login application is now:
- ✅ Fully containerized with Docker
- ✅ Encrypted database with SQLCipher
- ✅ Environment variable configuration
- ✅ GitHub Actions CI/CD automated
- ✅ Running in production
- ✅ Backed up and monitored
- ✅ Ready for team deployment

**Next Step:** Show your team this documentation and have them review the deployment process.
