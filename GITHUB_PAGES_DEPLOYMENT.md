# Step-by-Step Guide: Deploy Solow Convergence Report to GitHub Pages

## Prerequisites
- GitHub account
- Git installed on your computer
- Project code ready to push

## Step 1: Create or Use Existing GitHub Repository

### Option A: Create a New Repository on GitHub
1. Go to [github.com/new](https://github.com/new)
2. Enter repository name: `makroekonomia_solow_project`
3. Select **Public** (required for GitHub Pages on free accounts)
4. Click **Create repository**

### Option B: If Repository Already Exists
- Verify the repository is **Public** by checking Settings → Visibility

## Step 2: Configure Repository Settings for GitHub Pages

1. Go to your repository on GitHub
2. Click **Settings** (top menu)
3. Go to **Pages** (left sidebar)
4. Under "Build and deployment":
   - **Source**: Select "GitHub Actions"
   - This tells GitHub to deploy based on the workflow file
5. Click **Save**

## Step 3: Verify GitHub Actions Workflow File

The workflow file is already in place at `.github/workflows/pages.yml`

To verify it exists locally:
```powershell
Test-Path ".\.github\workflows\pages.yml"
```

If it doesn't exist, create it with the deployment configuration included in the project.

## Step 4: Push Code to GitHub

### Set Remote URL (if not already set)
```powershell
git remote add origin https://github.com/YOUR_USERNAME/makroekonomia_solow_project.git
```

### Push to Main Branch
```powershell
git add .
git commit -m "Add Solow convergence project with Polish report generation"
git push -u origin main
```

If you have a different branch name (like `master`), replace `main` with your branch name:
```powershell
git branch -M main
git push -u origin main
```

## Step 5: Monitor GitHub Actions Deployment

1. Go to your GitHub repository
2. Click **Actions** (top menu)
3. You should see a workflow named "Deploy GitHub Pages"
4. Click on the latest run to view the deployment status
5. Expected steps:
   - ✅ Set up Python 3.11
   - ✅ Install dependencies
   - ✅ Run pytest tests
   - ✅ Generate report
   - ✅ Deploy to GitHub Pages

## Step 6: Access Your Report

Once deployment completes:
- Your report will be available at: `https://YOUR_USERNAME.github.io/makroekonomia_solow_project/`
- Direct link to report: `https://YOUR_USERNAME.github.io/makroekonomia_solow_project/`

Wait a few minutes for the first deployment (typically 1-3 minutes).

## Step 7: Verify Deployment

1. Visit your GitHub Pages URL
2. You should see `index.html` with the Solow convergence analysis
3. Charts should display correctly
4. Polish language content should render properly

## Step 8: Future Updates

Whenever you make changes and push to GitHub:
```powershell
git add .
git commit -m "Update convergence analysis"
git push
```

GitHub Actions will automatically:
1. Run tests
2. Generate the latest report
3. Deploy to GitHub Pages within 1-3 minutes

## Troubleshooting

### Deployment Failed
- Check **Actions** tab to see error messages
- Common issues:
  - Tests failing: Run `python3.exe -m pytest -q` locally
  - Data fetch error: Check World Bank API is accessible
  - Missing dependencies: Verify `requirements.txt` is up to date

### Report Not Updating
- GitHub Pages can cache for up to 10 minutes
- Hard refresh: `Ctrl+Shift+R` (or `Cmd+Shift+R` on Mac)

### Cannot Find Deployment Logs
- Go to **Actions** → **Deploy GitHub Pages** workflow
- Click latest run
- Expand steps to see detailed logs

## Important Notes

✅ **The `.github/workflows/pages.yml` is already configured and ready to use**

✅ **The project automatically:**
- Installs dependencies
- Runs all tests
- Generates the report with real World Bank data
- Deploys everything to GitHub Pages

✅ **Report updates automatically** when you push changes to main branch

---

**Example**: After completing these steps, your report will be live at:
- `https://github.com/username/makroekonomia_solow_project` (repository)
- `https://username.github.io/makroekonomia_solow_project/` (live report)
