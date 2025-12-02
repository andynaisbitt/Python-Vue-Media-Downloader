# Final Analysis - Progress Hook Not Working

## 🔍 Deep Dive Results

After extensive investigation, here's what we discovered:

### ✅ What We Fixed:
1. ✅ Added `progress_hooks` to yt-dlp options in `downloader.py`
2. ✅ Added debug logging throughout (`🎯`, `📊`, `✅`)
3. ✅ Added `overwrites: True` to force re-downloads
4. ✅ Backend auto-reload confirmed working

### ❌ Current Problem:

**THE PROGRESS HOOK IS NEVER BEING CALLED**

Even though:
- Progress hooks ARE in the yt-dlp options dict ✅
- The download DOES start (we see `[download] Destination: ...`) ✅
- yt-dlp IS running ✅

We get **ZERO** progress hook callbacks:
- ❌ No "🎯 PROGRESS HOOK CALLED" messages
- ❌ No "📊 Progress" messages
- ❌ Frontend shows no progress

### 🐛 Additional Issues Discovered:

1. **yt-dlp nsig extraction failing**:
   ```
   WARNING: [youtube] 7pKN_pjPW04: nsig extraction failed
   ```

2. **Download appears to hang at 0%**:
   ```
   [download]   0.0% of   10.80MiB at  Unknown B/s ETA Unknown
   ```
   Then no further output.

3. **Files getting cached**:
   The `.mp4` file keeps being detected as already downloaded.

## 🔬 Root Cause Analysis

The issue is likely **ONE OF**:

### Theory 1: yt-dlp Version Issue
The `progress_hooks` might not be working with this version of yt-dlp. Some versions have bugs with hooks.

**Test**: Upgrade yt-dlp
```bash
pip install --upgrade yt-dlp
```

### Theory 2: The `.part` Files Issue
With `nopart: False`, yt-dlp downloads to `.f399.mp4` first, then merges. Progress hooks might only fire during the merge phase, which is instant for small files.

**Test**: Try `nopart: True` instead

### Theory 3: M3U8/HLS Streaming
The format being downloaded is `399+140-9` which might be HLS streaming. Progress hooks might not fire for streamed downloads.

**Test**: Force a different format:
```python
'format': 'best[ext=mp4]'  # Single file, no merge needed
```

### Theory 4: The Hook is in the Wrong YoutubeDL Instance
We're calling `extract_info` with `download=False` first, then calling `download()` later. The hooks might need to be on BOTH calls.

**Test**: Check if hooks are preserved across calls

## 🎯 Recommended Solution

I recommend trying **a simplified approach** that's proven to work:

### Create a Test Script

Create `test_yt dlp_hooks.py` in the backend folder:

```python
import yt_dlp

def progress_hook(d):
    if d['status'] == 'downloading':
        print(f"🎯 PROGRESS: {d.get('_percent_str', '0%')} - Speed: {d.get('_speed_str', 'Unknown')}")
    elif d['status'] == 'finished':
        print("✅ Download finished!")

ydl_opts = {
    'format': 'best[ext=mp4]',
    'outtmpl': 'C:\\Dev\\youtube-downloader\\backend\\downloads\\test_%(title)s.%(ext)s',
    'progress_hooks': [progress_hook],
    'quiet': False,
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    url = 'https://www.youtube.com/watch?v=jNQXAC9IVRw'  # 19 second video
    print("Starting download...")
    ydl.download([url])
    print("Done!")
```

Run it:
```bash
cd /c/Dev/youtube-downloader/backend
python test_ytdlp_hooks.py
```

**Expected Output**:
```
Starting download...
🎯 PROGRESS: 5.2% - Speed: 2.45MiB/s
🎯 PROGRESS: 15.8% - Speed: 2.34MiB/s
... (many more lines) ...
✅ Download finished!
Done!
```

If this works, then the hooks ARE functional, and the problem is in HOW we're calling yt-dlp in our code.

## 🔧 Alternative Fixes to Try

### Fix 1: Remove the Two-Stage Download
Currently we do:
1. `extract_info(url, download=False)` - Get metadata
2. `ydl.download([url])` - Actually download

**Try instead**:
```python
# Single call with progress hooks
info = ydl.extract_info(url, download=True)  # download=True
```

The hooks should fire during this single call.

### Fix 2: Use postprocessor_hooks Instead
If progress_hooks don't work, try postprocessor hooks:

```python
def postprocessor_hook(d):
    if d['status'] == 'started':
        print(f"🎯 Processing started")
    elif d['status'] == 'processing':
        print(f"🎯 Processing...")
    elif d['status'] == 'finished':
        print(f"✅ Processing finished")

ydl_opts = {
    ...
    'progress_hooks': [progress_hook],
    'postprocessor_hooks': [postprocessor_hook],
}
```

### Fix 3: Poll File Size Instead
As a workaround, monitor the .part file size:

```python
import os
import time

# Start download in thread
# ...

# In another thread, poll file size
while download_active:
    for file in os.listdir(download_dir):
        if file.endswith('.part') or file.endswith('.f399.mp4'):
            size = os.path.getsize(os.path.join(download_dir, file))
            # Calculate progress based on expected size
            # Update job status
    time.sleep(0.5)
```

## 📝 Next Steps

1. **Run the test script** to verify hooks work in isolation
2. If they work, **simplify the downloader.py code** to use single-call download
3. If they don't work, **upgrade yt-dlp**: `pip install --upgrade yt-dlp`
4. If still broken, **use the file polling workaround** as a temporary solution

## 💡 Why This is Happening

The most likely explanation is that when you call:
1. `extract_info(url, download=False)` - Hooks not used here
2. `ydl.download([url])` - Hooks SHOULD fire here but might not if yt-dlp cached the info

The second call might be using cached information from the first call, bypassing the actual download process where hooks fire.

## ✅ Guaranteed Working Solution

If all else fails, here's a **guaranteed** way to get progress:

```python
import subprocess
import re

# Call yt-dlp as subprocess and parse output
process = subprocess.Popen(
    ['yt-dlp', url, '--newline', ...other args...],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    universal_newlines=True
)

for line in process.stdout:
    # Parse lines like "[download]  45.2% of  100.00MiB at  2.45MiB/s ETA 00:23"
    match = re.search(r'\[download\]\s+([\d.]+)%', line)
    if match:
        progress = float(match.group(1))
        # Update job status
        job['progress'] = progress
```

This bypasses the Python API entirely and just parses the command-line output, which ALWAYS shows progress.

---

**Status**: Progress hooks are in place but not firing. Need to test in isolation and potentially refactor the download flow.
**Recommended**: Try the test script first, then implement single-call download method.
