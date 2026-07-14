# How to Push Music App to GitHub

The code is ready to push. Here are the steps:

## Step 1: Create Repository on GitHub
1. Go to https://github.com/new
2. Repository name: `music-app`
3. Description: "Full-stack music streaming app with YouTube integration"
4. Select: **Public**
5. ⚠️ Do NOT check "Initialize with README" (we have one)
6. Click **Create repository**

## Step 2: Push Code
Once the repository is created, run these commands:

```bash
# Change to project directory
cd /path/to/music-app

# Set your Git config
git config user.email "your-email@example.com"
git config user.name "Your Name"

# Add remote
git remote add origin https://github.com/shafiathussain20-pixel/music-app.git

# Push code
git branch -M main
git push -u origin main
```

## Step 3: Verify Push
- Visit https://github.com/shafiathussain20-pixel/music-app
- Confirm all files are there (README.md, docker-compose.yml, backend/, frontend/, .github/workflows/)

## Step 4: Setup GitHub Actions
1. Add GitHub Secrets for CI/CD:
   - Go to Settings → Secrets and variables → Actions
   - Click "New repository secret"
   - Add:
     - `DOCKER_USERNAME` = your Docker Hub username
     - `DOCKER_PASSWORD` = your Docker Hub token

2. CI/CD will automatically run on push to main

## Step 5: Enable GitHub Pages (Optional)
If you want to host docs:
- Settings → Pages
- Source: Deploy from a branch
- Branch: main, folder: / (root)

## Troubleshooting

**403 Forbidden Error:**
- Create new Personal Access Token at https://github.com/settings/tokens
- Select 'repo' scope
- Use: `git push -u https://USERNAME:TOKEN@github.com/USERNAME/music-app.git main`

**Repository not found:**
- Verify repo exists at https://github.com/shafiathussain20-pixel/music-app
- Double-check spelling

**Auth failed:**
- Use Personal Access Token instead of password
- Newer GitHub requires token-based auth

## Project Files Structure on GitHub

```
music-app/
├── README.md (project overview)
├── DEPLOYMENT.md (deployment guide)
├── docker-compose.yml (all services)
├── .gitignore (excluded files)
├── .github/
│   └── workflows/
│       └── ci-cd.yml (GitHub Actions)
├── backend/
│   ├── server.js
│   ├── database.js
│   ├── models/
│   ├── Dockerfile
│   ├── package.json
│   └── .env.example
├── frontend/
│   ├── src/
│   ├── public/
│   ├── Dockerfile
│   ├── package.json
│   └── .env.example
```

## Next Steps After Push

1. **Enable Actions** (auto-enabled if public)
2. **Add Secrets** for Docker Hub (if CI/CD builds images)
3. **Deploy** - Use Actions or deploy manually with Docker
4. **Monitor** - Check Actions tab for CI/CD status
