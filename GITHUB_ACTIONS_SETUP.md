# GitHub Actions CI/CD Setup

## Overview

This project includes automated CI/CD with GitHub Actions that:
- ✓ Runs unit tests on every push and pull request
- ✓ Performs security scanning with Bandit and TruffleHog
- ✓ Builds Docker images automatically
- ✓ Pushes to Docker Hub on successful tests
- ✓ Uses GitHub Actions secrets for secure credential management

## Prerequisites

1. **GitHub Repository** with Actions enabled
2. **Docker Hub Account** (or any Docker registry)
3. **Docker Hub Personal Access Token** for automated pushes

## Setup Instructions

### Step 1: Get Docker Hub Personal Access Token

1. Go to https://hub.docker.com/settings/security
2. Click "New Access Token"
3. Give it a name: `github-actions`
4. Set permissions to "Read & Write"
5. Click "Generate"
6. Copy the token (you won't be able to see it again)

### Step 2: Add GitHub Actions Secrets

1. Go to your GitHub repository
2. Click "Settings" (top right)
3. Click "Secrets and variables" → "Actions" (left sidebar)
4. Click "New repository secret"

Add these secrets:

| Secret Name | Value |
|-------------|-------|
| `DOCKER_USERNAME` | Your Docker Hub username |
| `DOCKER_PASSWORD` | Your Docker Hub personal access token |

**Example:**
- Secret name: `DOCKER_USERNAME`
- Secret value: `your-docker-username`

Then:
- Secret name: `DOCKER_PASSWORD`
- Secret value: `dckr_pat_xxxxxxxxxxxxxxxxxxxx`

### Step 3: Verify Workflow

The workflow file is already in `.github/workflows/ci-cd.yml`

Trigger a workflow by pushing code:

```bash
git add .
git commit -m "Enable CI/CD"
git push origin main
```

Go to your repository → "Actions" tab to see the workflow running.

## Workflow Jobs

### 1. Test Job
- **Runs on:** Ubuntu Latest
- **Steps:**
  - Checkout code
  - Set up Python 3.11
  - Install dependencies
  - Run unit tests
  - Generate coverage report

### 2. Security Scan Job
- **Runs on:** Ubuntu Latest
- **Tools:**
  - **Bandit:** Checks for security issues in Python code
  - **TruffleHog:** Searches for accidentally committed secrets

### 3. Build Job
- **Runs on:** Ubuntu Latest
- **Requires:** Test and Security Scan to pass
- **Steps:**
  - Build Docker image
  - Run tests in Docker container
  - Push to Docker Hub (only on main and develop branches)

### 4. Notify Job
- **Runs on:** Ubuntu Latest
- **Reports:** Overall success/failure status

## Branch Strategies

### Main Branch
- All pushes to `main` trigger the pipeline
- On success, image is tagged: `username/login-app:latest`
- Also tagged with commit SHA: `username/login-app:commit-sha`

### Develop Branch
- All pushes to `develop` trigger the pipeline
- On success, image is tagged: `username/login-app:develop`
- Also tagged with commit SHA: `username/login-app:dev-commit-sha`

### Feature Branches
- Tests run but image is NOT pushed to registry
- Security scans still run
- Good for validating changes before merging

## Using GitHub Actions with Docker

### Pull Latest Image After Deploy

```bash
# After CI/CD pipeline completes
docker pull your-username/login-app:latest
docker run -e DB_PASSWORD="your_password" login-app:latest
```

### Update docker-compose to use remote image

```yaml
version: '3.8'

services:
  login-app:
    image: your-username/login-app:latest
    environment:
      - DB_PASSWORD=${DB_PASSWORD}
    volumes:
      - ./users.db:/app/users.db
```

## Monitoring & Troubleshooting

### View Workflow Status

1. Go to "Actions" tab in your repository
2. Click on a workflow run to see details
3. Click on a job to see logs

### Common Issues

**"Authentication failed"**
- Verify `DOCKER_USERNAME` and `DOCKER_PASSWORD` secrets are set
- Ensure token has "Read & Write" permissions
- Check if token has expired

**"Tests failed in CI but pass locally"**
- Check Python version mismatch (CI uses 3.11)
- Verify all dependencies in `requirements.txt`
- Run `pip install -r requirements.txt` locally

**"Bandit security warnings"**
- Review security findings in "Security Scan" job
- Fix issues in code
- Push again to re-run

**"TruffleHog found secrets"**
- Check if real secrets were accidentally committed
- If false positive, add to `.trufflehog-suppress` (create if needed)
- Rotate credentials if real secret was found

### Viewing Logs

```bash
# Clone the repo and run locally to test
git clone https://github.com/your-username/login-app.git
cd login-app
python -m unittest test_app -v
```

## Advanced Configuration

### Skip CI/CD for Specific Commits

Add to commit message:

```bash
git commit -m "Minor docs update [skip ci]"
```

### Matrix Testing (Multiple Python Versions)

Edit `.github/workflows/ci-cd.yml`:

```yaml
jobs:
  test:
    strategy:
      matrix:
        python-version: ['3.9', '3.10', '3.11', '3.12']
    steps:
      - uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
```

### Scheduled Nightly Builds

Add to workflow YAML:

```yaml
on:
  schedule:
    - cron: '0 2 * * *'  # Run at 2 AM daily
  push:
    branches: [main]
```

### Deploy to Multiple Registries

Add to build job:

```yaml
- name: Push to GitHub Container Registry
  uses: docker/build-push-action@v5
  with:
    context: .
    push: true
    tags: ghcr.io/${{ github.repository }}:latest
    registry: ghcr.io
```

### Custom Slack Notifications

Add step to notify job:

```yaml
- name: Notify Slack on Failure
  if: failure()
  uses: slackapi/slack-github-action@v1
  with:
    webhook-url: ${{ secrets.SLACK_WEBHOOK }}
    payload: |
      {
        "text": "Build failed for ${{ github.repository }}"
      }
```

## Secrets Best Practices

1. **Never commit secrets** — `.gitignore` should include `.env`
2. **Use repository secrets** — Always use GitHub Actions secrets
3. **Rotate credentials regularly** — Change Docker Hub tokens quarterly
4. **Limit scope** — Give tokens minimum necessary permissions
5. **Audit access** — Review who has access to secrets
6. **Monitor usage** — Check for suspicious activity in Docker Hub

## Performance Optimization

### Cache Docker Layers

The workflow already uses GitHub Actions Docker layer caching:

```yaml
cache-from: type=gha
cache-to: type=gha,mode=max
```

This speeds up builds by caching layers between runs.

### Parallel Jobs

Jobs run in parallel when possible:
- Test and Security Scan run simultaneously
- Build waits for both to complete
- Notify runs at the end

## Integration with Pull Requests

When you create a PR:
1. CI/CD pipeline runs automatically
2. Tests must pass before merging
3. Required status checks can be enforced

To require status checks:
1. Go to Settings → Branches
2. Click "Add rule"
3. Select "main" branch
4. Check "Require status checks to pass"
5. Select "test" and "build" jobs

## Reference

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Build Push Action](https://github.com/docker/build-push-action)
- [Bandit Security Scanner](https://bandit.readthedocs.io/)
- [TruffleHog Secrets Detection](https://github.com/trufflesecurity/trufflehog)
