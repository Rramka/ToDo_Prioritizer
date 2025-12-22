# Setting Up Remote Repository

## Current Status
- ✅ Local git repository initialized
- ❌ No remote repository configured
- ❌ No commits made yet

## Steps to Create and Connect Remote Repository

### Option 1: GitHub (Recommended)

1. **Create a new repository on GitHub:**
   - Go to https://github.com/new
   - Repository name: `ToDo_Prioritizer` (or your preferred name)
   - Description: "Smart task prioritization tool with AI-powered breakdown"
   - Choose Public or Private
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
   - Click "Create repository"

2. **Copy the repository URL** from GitHub (it will look like):
   ```
   https://github.com/YOUR_USERNAME/ToDo_Prioritizer.git
   ```
   or
   ```
   git@github.com:YOUR_USERNAME/ToDo_Prioritizer.git
   ```

3. **Add remote and push:**
   ```bash
   # Add all files
   git add .

   # Make initial commit
   git commit -m "Initial commit: ToDo Prioritizer MVP"

   # Add remote repository
   git remote add origin https://github.com/YOUR_USERNAME/ToDo_Prioritizer.git

   # Push to remote
   git branch -M main
   git push -u origin main
   ```

### Option 2: GitLab

1. **Create a new project on GitLab:**
   - Go to https://gitlab.com/projects/new
   - Project name: `ToDo_Prioritizer`
   - Visibility: Public or Private
   - **DO NOT** initialize with README
   - Click "Create project"

2. **Copy the repository URL** and follow the same steps as GitHub

### Option 3: Other Git Hosting

- **Bitbucket**: https://bitbucket.org/repo/create
- **Azure DevOps**: Create a new repository in your project
- **Self-hosted**: Use your own Git server

## Quick Setup Script

After creating the repository on GitHub/GitLab, run:

```bash
# Replace YOUR_USERNAME and REPO_NAME with your actual values
REPO_URL="https://github.com/YOUR_USERNAME/REPO_NAME.git"

git add .
git commit -m "Initial commit: ToDo Prioritizer MVP - Complete full-stack application with AI-powered task prioritization"
git branch -M main
git remote add origin $REPO_URL
git push -u origin main
```

## After Setup

Your repository URL will be:
- **GitHub**: `https://github.com/YOUR_USERNAME/ToDo_Prioritizer`
- **GitLab**: `https://gitlab.com/YOUR_USERNAME/ToDo_Prioritizer`

## Verify Remote

After adding the remote, verify it:
```bash
git remote -v
```

You should see:
```
origin  https://github.com/YOUR_USERNAME/ToDo_Prioritizer.git (fetch)
origin  https://github.com/YOUR_USERNAME/ToDo_Prioritizer.git (push)
```

