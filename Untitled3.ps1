# Create downloader utility
$downloaderUtil = @"
import os
import yt_dlp
from typing import Dict, Any

def download_and_process(url: str, output_dir: str, **kwargs) -> Dict[str, Any]:
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Configure yt-dlp options
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'quiet': True,
        'progress': False,
        'no_warnings': True
    }

    # Handle format preference
    format_pref = kwargs.get('format', 'mp4')
    if format_pref == 'mp4':
        ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
    elif format_pref == 'mp3':
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        })

    # Handle quality preference
    quality = kwargs.get('quality', 'best')
    if quality != 'best':
        quality_map = {
            '1080p': '[height<=1080]',
            '720p': '[height<=720]',
            '480p': '[height<=480]',
        }
        if quality in quality_map:
            ydl_opts['format'] = f'bestvideo{quality_map[quality]}+bestaudio/best{quality_map[quality]}'

    # Handle subtitles
    if kwargs.get('subtitles', False):
        ydl_opts.update({
            'writesubtitles': True,
            'subtitleslangs': ['en'],
        })

    try:
        # Extract info first
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'video')
            duration = info.get('duration')
            
            # Download the video
            ydl.download([url])

            # Prepare result
            output_file = os.path.join(output_dir, f'{title}.{format_pref}')
            return {
                'success': True,
                'title': title,
                'duration': duration,
                'format': format_pref,
                'quality': quality,
                'output': output_file,
                'url': url
            }

    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'url': url
        }
"@
New-Item -ItemType Directory -Path "app/utils" -Force
Set-Content -Path "app/utils/downloader.py" -Value $downloaderUtil -NoNewline

# Create __init__.py files
$initFile = @"
# This file is intentionally empty to mark directory as Python package
"@
Set-Content -Path "app/utils/__init__.py" -Value $initFile -NoNewline

# Update requirements.txt
$requirements = @"
flask==2.0.1
flask-cors==3.0.10
flask-login==0.5.0
python-dotenv==0.19.0
yt-dlp==2023.12.30
PyJWT==2.1.0
"@
Set-Content -Path "requirements.txt" -Value $requirements -NoNewline

# Create the config file if it doesn't exist
$configFile = @"
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'downloads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max-limit
"@
Set-Content -Path "config.py" -Value $configFile -NoNewline

# Setup virtual environment and install dependencies
Write-Host "Setting up Python virtual environment..."
python -m venv venv
.\venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt

Write-Host "`n✨ Backend fixed! The backend should now work correctly."
Write-Host "Remember to:"
Write-Host "1. Activate the virtual environment: .\venv\Scripts\activate"
Write-Host "2. Run the backend: python run.py"
Write-Host "3. The API will be available at http://localhost:5000"