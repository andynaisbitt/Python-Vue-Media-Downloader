# 🧹 How to Remove Large Files from Git History

Your Git repository contains large files that exceed GitHub's 100MB limit. Here's how to clean them up.

---

## 🚨 Problem Files

The following files are too large for GitHub:
- `backend/ffmpeg/ffmpeg.exe` (121.38 MB)
- `backend/ffmpeg/ffprobe.exe` (121.25 MB)
- `backend/ffmpeg/ffplay.exe` (121.23 MB)
- `latest backup.zip` (173.94 MB)

---

## ✅ Solution: Use BFG Repo Cleaner (Recommended)

BFG is faster and easier than git filter-branch.

### Step 1: Install BFG

**Download:** https://rtyley.github.io/bfg-repo-cleaner/

**Or with package manager:**
```bash
# Windows (Chocolatey)
choco install bfg-repo-cleaner

# macOS (Homebrew)
brew install bfg

# Java required (download from https://java.com)
```

### Step 2: Clone a Fresh Mirror

```bash
git clone --mirror https://github.com/andynaisbitt/Python-Vue-Media-Downloader.git
cd Python-Vue-Media-Downloader.git
```

### Step 3: Run BFG to Remove Large Files

```bash
# Remove specific files
bfg --delete-files ffmpeg.exe
bfg --delete-files ffprobe.exe
bfg --delete-files ffplay.exe
bfg --delete-files "latest backup.zip"

# Or remove all files over 100MB
bfg --strip-blobs-bigger-than 100M
```

### Step 4: Clean and Push

```bash
git reflog expire --expire=now --all
git gc --prune=now --aggressive
git push --force
```

---

## 🔧 Alternative: Manual Git Filter-Branch

If you can't use BFG, use git filter-branch (slower):

### For Windows (PowerShell):

```powershell
# Remove FFmpeg executables
git filter-branch --force --index-filter "git rm --cached --ignore-unmatch backend/ffmpeg/ffmpeg.exe backend/ffmpeg/ffprobe.exe backend/ffmpeg/ffplay.exe" --prune-empty --tag-name-filter cat -- --all

# Remove backup files
git filter-branch --force --index-filter "git rm --cached --ignore-unmatch 'latest backup.zip'" --prune-empty --tag-name-filter cat -- --all

# Cleanup
git for-each-ref --format="delete %(refname)" refs/original | git update-ref --stdin
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# Force push
git push origin --force --all
git push origin --force --tags
```

### For macOS/Linux (Bash):

```bash
#!/bin/bash

# Remove large files
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch backend/ffmpeg/*.exe "latest backup.zip"' \
  --prune-empty --tag-name-filter cat -- --all

# Cleanup
git for-each-ref --format='delete %(refname)' refs/original | git update-ref --stdin
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# Force push
git push origin --force --all
git push origin --force --tags
```

---

## 🎯 Easiest Solution: Start Fresh

If the repository is new and doesn't have important history:

### Step 1: Backup Your Code
```bash
# Copy entire folder to a backup location
cp -r C:\Dev\youtube-downloader C:\Dev\youtube-downloader-backup
```

### Step 2: Delete Local Git History
```bash
cd C:\Dev\youtube-downloader
rm -rf .git
```

### Step 3: Initialize Fresh Repository
```bash
git init
git add .
git commit -m "Initial commit - v1.0.0"
```

### Step 4: Force Push to GitHub
```bash
git remote add origin https://github.com/andynaisbitt/Python-Vue-Media-Downloader.git
git branch -M main
git push -u origin main --force
```

---

## ⚠️ Important Notes

1. **Backup First!** Make a complete copy before running any commands
2. **Force Push Warning:** This rewrites history - collaborators will need to re-clone
3. **Update .gitignore:** Already done! Large files are now ignored
4. **Verify After:** Check file sizes with `git ls-files -l | sort -nk 2 | tail -10`

---

## 🔍 Verify Cleanup

After cleanup, verify large files are gone:

```bash
# Check largest files in repository
git ls-files -l | sort -nk 2 | tail -10

# Check specific file is gone
git log --all -- backend/ffmpeg/ffmpeg.exe
# Should return nothing

# Check repository size
git count-objects -vH
```

---

## ✅ Post-Cleanup Checklist

- [ ] Large files removed from Git history
- [ ] `.gitignore` updated (already done)
- [ ] Successfully pushed to GitHub
- [ ] FFmpeg setup instructions in `backend/ffmpeg/README.md`
- [ ] Verification script works (`python verify-setup.py`)
- [ ] Users know to download FFmpeg separately

---

## 📚 Additional Resources

- **BFG Repo Cleaner:** https://rtyley.github.io/bfg-repo-cleaner/
- **Git LFS (for future):** https://git-lfs.github.com/
- **GitHub File Size Limits:** https://docs.github.com/en/repositories/working-with-files/managing-large-files

---

## 💡 Preventing This in Future

1. Always check `.gitignore` before committing large files
2. Use `git add -p` to review changes before staging
3. Run verification: `git ls-files -s | awk '$4 > 100000000'` before pushing
4. Consider Git LFS for large binary files (if needed in repo)

---

**Need Help?** The `.gitignore` is already updated to prevent this happening again!
