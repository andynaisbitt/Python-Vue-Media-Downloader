# Debug Guide - Download Progress Issue

## Current Status
✅ Backend updated to send `downloaded_bytes` and `total_bytes`
✅ Frontend store updated to capture byte data
✅ DownloadItem component enhanced with smooth animations
✅ QueueList updated to use DownloadItem component
✅ Debug logging added throughout the flow

## How to Test

### 1. Open the App
- Frontend: http://localhost:5173
- Open browser console (F12)

### 2. Start a Download
Use any valid YouTube URL, for example:
- Short video: https://www.youtube.com/watch?v=dQw4w9WgXcQ
- Format: MP4
- Quality: best

### 3. Watch the Console Output

You should see logs like this:

```
📊 Progress Update: {
  status: "downloading",
  progress: 45.2,
  speed: 2457600,  // bytes per second
  eta: 32,         // seconds
  downloaded_bytes: 47382528,  // ~45.2 MB
  total_bytes: 104857600       // ~100 MB
}

🎯 DownloadItem Progress Update: {
  id: 1733163245678,
  title: "Video Title",
  progress: 45.2,
  status: "downloading",
  speed: 2457600,
  downloaded_bytes: 47382528,
  total_bytes: 104857600
}
```

## Troubleshooting

### Issue 1: No logs appearing
**Problem**: Backend isn't responding
**Solution**: Check backend is running on http://127.0.0.1:5000

```bash
cd /c/Dev/youtube-downloader/backend
python run.py
```

### Issue 2: `downloaded_bytes` and `total_bytes` are null/undefined
**Problem**: Backend isn't sending byte data
**Solutions**:
1. Check backend logs for errors
2. Verify yt-dlp is providing byte information
3. Some videos don't report total size during download

**Expected behavior**: Most videos will have byte data, but some live streams or special formats may not.

### Issue 3: Progress shows but no byte display
**Problem**: Frontend isn't receiving/displaying bytes
**Check**:
1. Console logs show bytes are being received
2. DownloadItem component's computed properties
3. Browser console for any Vue errors

### Issue 4: Progress bar doesn't animate smoothly
**Problem**: CSS transitions not working
**Check**:
1. Browser DevTools → Elements → check for transition classes
2. Check if `smoothProgress` ref is updating
3. Verify 700ms transition is in the CSS

### Issue 5: Speed graph not showing
**Problem**: Need at least 2 speed readings
**Expected**: Graph appears after 4-6 seconds of downloading

## What You Should See

### During Download:

```
┌─────────────────────────────────────────────────────────┐
│ 📹 Video Title                                          │
│ ───────────────────────────────────────────────────── │
│ Size: 100.0 MB • Duration: 5:23 • Format: MP4         │
│                                                         │
│ [████████████████████░░░░░░░░░░░░░░░] 67%             │
│     ✨ shimmer animation moving across                 │
│                                                         │
│ 🟣 67.2 MB / 100.0 MB                                  │
│                                                         │
│ ⬇️ 2.4 MB/s      ⏱️ 14s remaining                     │
│                                                         │
│ ▁▂▃▅▇█▇▆▄▃▂▁▂▃▅▆▇█▆▅ ← Speed graph                    │
└─────────────────────────────────────────────────────────┘
```

### Status Badge Colors:
- 🔵 Blue: Queued/Starting
- 🟣 Purple: Downloading
- 🟡 Yellow: Processing
- 🟢 Green: Completed
- 🔴 Red: Failed

## Expected Console Output Timeline

```
[0s]  📊 Progress Update: { status: "starting", progress: 0 }
[1s]  🎯 DownloadItem: { status: "starting", progress: 0 }

[2s]  📊 Progress Update: { status: "downloading", progress: 5.2, speed: 1245000, ... }
[2s]  🎯 DownloadItem: { progress: 5.2, downloaded_bytes: 6543210, total_bytes: 125829120 }

[4s]  📊 Progress Update: { status: "downloading", progress: 15.8, speed: 2134000, ... }
[4s]  🎯 DownloadItem: { progress: 15.8, downloaded_bytes: 19876543, total_bytes: 125829120 }

...continues every 2 seconds...

[45s] 📊 Progress Update: { status: "processing", progress: 100 }
[45s] 🎯 DownloadItem: { status: "processing", progress: 100 }

[48s] 📊 Progress Update: { status: "completed", result: {...} }
[48s] 🎯 DownloadItem: { status: "completed" }
```

## Backend Debug

To add backend logging, check your Flask terminal:

```python
# Should see in backend terminal:
INFO: Download starting for job_id: abc123
INFO: Progress: 25.5% (32MB/125MB) @ 2.4 MB/s
INFO: Progress: 50.2% (63MB/125MB) @ 2.3 MB/s
INFO: Download completed: video_title.mp4
```

## Common Issues & Fixes

### 1. "Progress jumps from 0 to 100"
- Check: Are you seeing status updates in console?
- Check: Is polling interval too slow? (default: 2000ms)
- Fix: Reduce polling interval in `download.js` line 150

### 2. "No byte information shown"
- Check: Console logs for `downloaded_bytes` and `total_bytes`
- Check: Backend is sending these fields
- Note: Some videos don't provide size until download starts

### 3. "Animations not smooth"
- Check: Browser DevTools performance tab
- Check: CSS transition is 700ms (line 48 in DownloadItem.vue)
- Check: `smoothProgress` ref is updating

### 4. "Speed graph not appearing"
- Need: At least 2 speed readings (4+ seconds of download)
- Check: `speedHistory` array in console
- Check: Speed is > 0 in backend response

## Next Steps

1. **Test with a real download**
   - Open http://localhost:5173
   - Paste a YouTube URL
   - Start download
   - **Watch browser console for logs**

2. **Share console output**
   - If it's not working, copy/paste the console logs
   - Include any error messages
   - Include network tab (F12 → Network) showing API calls

3. **Check backend terminal**
   - Any Python errors?
   - Is yt-dlp providing progress data?

---

**Quick Test URLs:**
- Short (< 1 min): https://www.youtube.com/watch?v=jNQXAC9IVRw
- Medium (5-10 min): https://www.youtube.com/watch?v=dQw4w9WgXcQ
- Long (30+ min): Any podcast or lecture video

**Expected Download Time:**
- Short video: 5-15 seconds (fast, but should still see progress)
- Medium video: 30-60 seconds (perfect for testing animations)
- Long video: 2-5 minutes (best for testing sustained progress)
