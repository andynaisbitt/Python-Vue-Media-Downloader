#!/bin/bash
# Script to remove large files from Git history
# This permanently removes files from all commits

echo "=========================================="
echo "Git Large File Cleanup Script"
echo "=========================================="
echo ""
echo "This will remove the following from Git history:"
echo "  - backend/ffmpeg/*.exe files"
echo "  - *.zip backup files"
echo ""
echo "WARNING: This rewrites Git history!"
echo "Press Ctrl+C to cancel, or Enter to continue..."
read

echo ""
echo "Step 1: Removing large files from Git history..."
echo ""

# Remove FFmpeg executables
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch backend/ffmpeg/ffmpeg.exe backend/ffmpeg/ffprobe.exe backend/ffmpeg/ffplay.exe' \
  --prune-empty --tag-name-filter cat -- --all

# Remove backup zip files
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch "latest backup.zip" *.zip' \
  --prune-empty --tag-name-filter cat -- --all

echo ""
echo "Step 2: Cleaning up refs..."
git for-each-ref --format='delete %(refname)' refs/original | git update-ref --stdin
git reflog expire --expire=now --all
git gc --prune=now --aggressive

echo ""
echo "=========================================="
echo "Cleanup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Verify the cleanup: git log --all -- backend/ffmpeg/*.exe"
echo "2. Force push to GitHub: git push origin --force --all"
echo "3. Force push tags: git push origin --force --tags"
echo ""
echo "WARNING: Anyone who has cloned the repo will need to re-clone!"
