# FFmpeg Setup for YouTube Video Downloader

## 📦 Why FFmpeg?

FFmpeg is required for:
- **Video format conversion** (AVI, MKV, etc.)
- **Audio extraction** (MP3, AAC, WAV)
- **Video merging** (combining separate video/audio streams)
- **Quality optimization** and codec processing

---

## 🚀 Quick Setup

### Option 1: Download FFmpeg to This Folder (Recommended)

1. **Download FFmpeg** for your platform:
   - **Windows**: https://www.gyan.dev/ffmpeg/builds/
     - Download: `ffmpeg-release-essentials.zip`
   - **macOS**: https://evermeet.cx/ffmpeg/
   - **Linux**: Use package manager (see below)

2. **Extract the binaries** to this folder (`backend/ffmpeg/`):
   ```
   backend/ffmpeg/
   ├── ffmpeg.exe (or ffmpeg on macOS/Linux)
   ├── ffprobe.exe (or ffprobe on macOS/Linux)
   └── README.md (this file)
   ```

3. **Verify installation**:
   ```bash
   # Windows
   .\backend\ffmpeg\ffmpeg.exe -version

   # macOS/Linux
   ./backend/ffmpeg/ffmpeg -version
   ```

4. **You're done!** The app will automatically detect FFmpeg in this folder.

---

### Option 2: System-Wide Installation

If you prefer to install FFmpeg system-wide:

#### Windows
```powershell
# Using Chocolatey
choco install ffmpeg

# Using Scoop
scoop install ffmpeg

# Manual installation
# 1. Download from https://www.gyan.dev/ffmpeg/builds/
# 2. Extract to C:\ffmpeg
# 3. Add C:\ffmpeg\bin to PATH
```

#### macOS
```bash
# Using Homebrew
brew install ffmpeg

# Using MacPorts
sudo port install ffmpeg
```

#### Linux
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install ffmpeg

# Fedora
sudo dnf install ffmpeg

# Arch Linux
sudo pacman -S ffmpeg
```

---

## 🔧 How It Works

The YouTube downloader checks for FFmpeg in this order:

1. **Local folder** (`backend/ffmpeg/ffmpeg.exe` or `backend/ffmpeg/ffmpeg`)
2. **System PATH** (if installed system-wide)
3. **Fallback** (limited functionality without FFmpeg)

If FFmpeg is not found:
- Basic MP4 downloads may still work
- Audio extraction and format conversion will fail
- You'll see warnings in the console

---

## 📋 What Files Are Needed?

### Minimum Required (Windows)
```
backend/ffmpeg/
├── ffmpeg.exe     # Main binary (video/audio processing)
└── ffprobe.exe    # Media information tool
```

### Minimum Required (macOS/Linux)
```
backend/ffmpeg/
├── ffmpeg     # Main binary (executable)
└── ffprobe    # Media information tool
```

### Optional
```
backend/ffmpeg/
└── ffplay.exe/ffplay    # Media player (not used by this app)
```

---

## ⚠️ Important Notes

### File Size Warning
- FFmpeg binaries are **~100-200 MB** in size
- They are **excluded from Git** (see `.gitignore`)
- Each user must download them separately

### Why Not Included in Repo?
- ❌ Large files slow down Git operations
- ❌ GitHub has file size limits (100MB)
- ❌ Different platforms need different binaries
- ✅ Users can choose system-wide or local installation

---

## 🧪 Testing FFmpeg

After installation, test if it works:

```bash
# Navigate to backend directory
cd backend

# Test FFmpeg
python -c "import os; print('FFmpeg found!' if os.path.exists('ffmpeg/ffmpeg.exe') or os.path.exists('ffmpeg/ffmpeg') else 'FFmpeg not found')"

# Or start the app and check console logs
python run.py
# Look for: "FFmpeg found, using custom location"
```

---

## 🔗 Download Links

### Official Sources
- **FFmpeg Official**: https://ffmpeg.org/download.html
- **Windows Builds**: https://www.gyan.dev/ffmpeg/builds/
- **macOS Builds**: https://evermeet.cx/ffmpeg/
- **Documentation**: https://ffmpeg.org/documentation.html

### Recommended Windows Build
- **URL**: https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip
- **Size**: ~120 MB
- **Contains**: ffmpeg.exe, ffprobe.exe, ffplay.exe

---

## ❓ Troubleshooting

### "FFmpeg not found" error

**Check 1**: Is FFmpeg in this folder?
```bash
ls backend/ffmpeg/
# Should see ffmpeg.exe (Windows) or ffmpeg (macOS/Linux)
```

**Check 2**: Are the files executable (macOS/Linux)?
```bash
chmod +x backend/ffmpeg/ffmpeg
chmod +x backend/ffmpeg/ffprobe
```

**Check 3**: Is FFmpeg in system PATH?
```bash
# Windows
where ffmpeg

# macOS/Linux
which ffmpeg
```

**Check 4**: Are you using the right platform's binary?
- ❌ Don't use Windows `.exe` files on macOS/Linux
- ❌ Don't use macOS/Linux binaries on Windows

### "Permission denied" error (macOS/Linux)
```bash
chmod +x backend/ffmpeg/ffmpeg
chmod +x backend/ffmpeg/ffprobe
```

### "File not found" error
- Ensure binaries are directly in `backend/ffmpeg/`, not in a subfolder
- Remove any version numbers from filenames (rename `ffmpeg-6.0.exe` to `ffmpeg.exe`)

---

## 💡 Pro Tips

1. **Portable Setup**: Keep FFmpeg in this folder for easy project sharing
2. **System-Wide**: Install system-wide if you use FFmpeg for other projects
3. **Auto-Update**: System-wide installations can be updated via package managers
4. **Docker**: If using Docker, FFmpeg can be installed in the container

---

## 📝 License

FFmpeg is licensed under the LGPL 2.1 or later.
See: https://ffmpeg.org/legal.html

This YouTube downloader uses FFmpeg as an external tool and does not redistribute it.

---

## ✅ Setup Complete?

Once FFmpeg is installed, you should see this in your console when running the app:

```
FFmpeg found, using custom location
```

Or if using system-wide installation:
```
FFmpeg not found at custom location, using system PATH
```

Both are fine! The app will work as long as FFmpeg is accessible.

---

**Need help?** Check the main README or open an issue on GitHub!
