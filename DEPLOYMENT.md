# Deployment Guide for Vercel

## Prerequisites
- GitHub account
- Vercel account (free tier available)

## Steps to Deploy

### 1. Push to GitHub
```bash
# Initialize git repository (if not already done)
git init

# Add all files
git add .

# Commit changes
git commit -m "Initial commit - LLC Formation Directory"

# Add GitHub remote (replace with your repository URL)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Push to GitHub
git push -u origin main
```

### 2. Deploy to Vercel
1. Go to [vercel.com](https://vercel.com) and sign up/login
2. Click "New Project"
3. Import your GitHub repository
4. Vercel will automatically detect it's a Python project
5. Click "Deploy"

### 3. Environment Variables (if needed)
If you have any environment variables, add them in the Vercel dashboard:
- Go to your project settings
- Navigate to "Environment Variables"
- Add any required variables

### 4. Custom Domain (Optional)
- In Vercel dashboard, go to "Domains"
- Add your custom domain (llcdirectory.org)
- Update DNS settings as instructed

## File Structure
```
llc-formation-website/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── vercel.json           # Vercel configuration
├── templates/            # HTML templates
├── static/              # CSS, JS, images
└── data/                # CSV data files
```

## Notes
- Vercel will automatically install dependencies from requirements.txt
- The vercel.json file routes all requests to app.py
- Static files are served automatically from the static/ directory
- The app will be available at your Vercel URL (e.g., your-project.vercel.app)
