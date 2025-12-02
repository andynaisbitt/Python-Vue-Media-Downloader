# Testing Instructions - Download Progress

## 🎯 Current Status

### ✅ Changes Applied:
1. Backend `download_manager.py` - Added debug logging to progress hook
2. Backend `downloader.py` - Added `progress_hooks` to yt-dlp options
3. Backend `downloader.py` - Added `overwrites: True` to force re-download
4. Backend `downloader.py` - Added `nopart: False` for .part files
5. Frontend - All UI enhancements ready
6. Backend - Reloaded with all changes

### 🐛 Issue Discovered:
**The previous test video was already downloaded**, so yt-dlp skipped it with:
```
[download] Claude Code Tutorial #9 - Claude Code with GitHub.mp4 has already been downloaded
```

This means the progress hook was never called!

### ✅ Fix Applied:
- Deleted the cached file
- Added `overwrites: True` to force re-downloads

## 🧪 How to Test (CRITICAL STEPS)

### Step 1: Clear Your Browser Cache
The frontend might have cached the old code. Do a **hard refresh**:
- Windows/Linux: `Ctrl + Shift + R`
- Mac: `Cmd + Shift + R`

### Step 2: Open Developer Console
Press `F12` and go to the Console tab

### Step 3: Start a NEW Download
Use a video you haven't downloaded yet, OR delete the existing file first.

**Test URLs:**
```
https://www.youtube.com/watch?v=jNQXAC9IVRw  (Me at the zoo - 19 seconds)
https://www.youtube.com/watch?v=9bZkp7q19f0  (Gangnam Style - 4:13)
https://www.youtube.com/watch?v=dQw4w9WgXcQ  (Rick Astley - 3:33)
```

### Step 4: Watch BOTH Consoles

#### Browser Console (Frontend):
You should see:
```javascript
📊 Progress Update: {status: 'starting', progress: 0, ...}
📊 Progress Update: {status: 'downloading', progress: 5.2, speed: 1245000, downloaded_bytes: 654321, total_bytes: 12582912}
📊 Progress Update: {status: 'downloading', progress: 15.8, ...}
🎯 DownloadItem Progress Update: {id: 1764..., progress: 15.8, ...}
... continues every 2 seconds ...
```

#### Backend Terminal:
You should see:
```
🎯 PROGRESS HOOK CALLED: downloading
📊 Progress: 5.2% | Downloaded: 654321 / 12582912 | Speed: 1245000 | ETA: 10
🎯 PROGRESS HOOK CALLED: downloading
📊 Progress: 15.8% | Downloaded: 1987654 / 12582912 | Speed: 2134000 | ETA: 5
... continues during download ...
🎯 PROGRESS HOOK CALLED: finished
✅ FINISHED - Moving to processing
```

## ❌ If Progress Hook is NOT Called

### Symptom:
Backend shows:
```
[download] filename.mp4 has already been downloaded
```

### Solution Options:

#### Option 1: Delete the file manually
```bash
cd /c/Dev/youtube-downloader/backend/downloads
ls  # see all files
rm "filename.mp4"  # delete the one you want to test
```

#### Option 2: Use a different video
Try a different YouTube URL that hasn't been downloaded yet.

#### Option 3: Verify overwrites setting
Check that `downloader.py` line 34 has:
```python
'overwrites': True,
```

## 🔍 Debugging Checklist

### Backend Not Showing Progress Hooks?

**Check 1**: Is the progress_hook function being registered?
Look for this in backend logs:
```python
'progress_hooks': [<function _run_download_job.<locals>.progress_hook at 0x...>]
```

**Check 2**: Is yt-dlp actually downloading?
If you see "has already been downloaded", the hook won't fire.

**Check 3**: Is the file actually downloading?
Look for lines like:
```
[download] Downloading item 1 of 1
[download]   0.0% of ~20.00MiB at  2.45MiB/s ETA 00:08
```

### Frontend Not Showing Progress?

**Check 1**: Is polling working?
Look for repeated API calls in Network tab (F12 → Network)
- Should see `/api/download/status/[job_id]` every 2 seconds

**Check 2**: Is the store updating?
Check console for "📊 Progress Update" logs

**Check 3**: Is the component receiving updates?
Check console for "🎯 DownloadItem Progress Update" logs

## 🎬 Expected Full Flow

### Backend Terminal:
```
1. Starting download for URL: https://...
2. yt-dlp options: {..., 'progress_hooks': [...], ...}
3. Extracting video information...
4. Video info extracted successfully:
5. Single video detected, starting download...
6. [download] Downloading item 1 of 1
7. 🎯 PROGRESS HOOK CALLED: downloading
8. 📊 Progress: 5.2% | Downloaded: ...
9. 🎯 PROGRESS HOOK CALLED: downloading
10. 📊 Progress: 15.8% | Downloaded: ...
   ... continues ...
11. 🎯 PROGRESS HOOK CALLED: finished
12. ✅ FINISHED - Moving to processing
13. Download completed successfully!
```

### Browser Console:
```
1. 📊 Progress Update: {status: 'starting', ...}
2. 📊 Progress Update: {status: 'downloading', progress: 5.2, ...}
3. 🎯 DownloadItem Progress Update: {progress: 5.2, ...}
4. 📊 Progress Update: {status: 'downloading', progress: 15.8, ...}
5. 🎯 DownloadItem Progress Update: {progress: 15.8, ...}
   ... continues ...
6. 📊 Progress Update: {status: 'processing', ...}
7. 📊 Progress Update: {status: 'completed', ...}
```

### Browser UI:
```
1. "Initializing download..." (pulsing purple bar)
2. Progress bar appears with shimmer effect
3. "45.2 MB / 120.5 MB" byte display
4. "2.4 MB/s" speed badge (green)
5. "32s remaining" ETA badge (blue)
6. Speed graph builds up (mini bars)
7. Progress bar smoothly moves to 100%
8. "Processing..." (yellow badge, spinning icon)
9. "Completed" (green badge)
```

## 🚨 Common Issues & Solutions

### Issue 1: "has already been downloaded"
**Solution**: Delete the file or use a different video

### Issue 2: No progress hook messages in backend
**Solution**: Check that `progress_hooks` is in yt-dlp options (see logs)

### Issue 3: Progress goes 0 → 100 instantly
**Solution**: File was cached or download was too fast (try larger video)

### Issue 4: Progress stuck at "starting"
**Solution**: Check backend logs for errors, might be video unavailable

### Issue 5: Console shows null/undefined bytes
**Solution**: Some videos don't report size, this is normal (progress % should still work)

## ✅ Success Criteria

You'll know it's working when you see:
1. ✅ Backend logs show multiple "🎯 PROGRESS HOOK CALLED: downloading" messages
2. ✅ Backend logs show actual byte progress (e.g., "Downloaded: 1234567 / 9876543")
3. ✅ Browser console shows progress updates every ~2 seconds
4. ✅ Browser UI shows progress bar smoothly animating
5. ✅ Browser UI shows "X.X MB / Y.Y MB" byte display
6. ✅ Browser UI shows speed graph with animated bars

## 📝 Report Results

Please share:
1. **Browser console logs** (all "📊" and "🎯" messages)
2. **Backend terminal logs** (all "🎯", "📊", "✅", "❌" messages)
3. **Screenshots or description** of what you see in the UI
4. **Video URL** you tested with
5. **Did the progress hook get called?** (yes/no - check for "🎯 PROGRESS HOOK CALLED")

---

**Current Status**: Backend running with debug logging, frontend ready, cache cleared
**Next Step**: Try downloading a NEW video and watch BOTH consoles!
