# PowerShell script to remove large files from Git history
# Run this in PowerShell (not CMD)

Write-Host "=========================================="
Write-Host "Git Large File Cleanup Script (Windows)"
Write-Host "=========================================="
Write-Host ""
Write-Host "This will remove the following from Git history:"
Write-Host "  - backend/ffmpeg/*.exe files"
Write-Host "  - *.zip backup files"
Write-Host ""
Write-Host "WARNING: This rewrites Git history!" -ForegroundColor Red
Write-Host "Press Ctrl+C to cancel, or Enter to continue..."
Read-Host

Write-Host ""
Write-Host "Step 1: Removing FFmpeg executables..." -ForegroundColor Yellow

git filter-branch --force --index-filter `
  "git rm --cached --ignore-unmatch backend/ffmpeg/ffmpeg.exe backend/ffmpeg/ffprobe.exe backend/ffmpeg/ffplay.exe" `
  --prune-empty --tag-name-filter cat -- --all

Write-Host ""
Write-Host "Step 2: Removing backup ZIP files..." -ForegroundColor Yellow

git filter-branch --force --index-filter `
  "git rm --cached --ignore-unmatch 'latest backup.zip'" `
  --prune-empty --tag-name-filter cat -- --all

Write-Host ""
Write-Host "Step 3: Cleaning up refs..." -ForegroundColor Yellow

git for-each-ref --format="delete %(refname)" refs/original | git update-ref --stdin
git reflog expire --expire=now --all
git gc --prune=now --aggressive

Write-Host ""
Write-Host "=========================================="
Write-Host "Cleanup Complete!" -ForegroundColor Green
Write-Host "=========================================="
Write-Host ""
Write-Host "Next steps:"
Write-Host "1. Verify: git log --all -- backend/ffmpeg/ffmpeg.exe"
Write-Host "2. Force push: git push origin --force --all"
Write-Host "3. Force push tags: git push origin --force --tags"
Write-Host ""
Write-Host "WARNING: Anyone who has cloned will need to re-clone!" -ForegroundColor Red
