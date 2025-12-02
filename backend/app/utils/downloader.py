import os
import yt_dlp
from typing import Dict, Any, List

def fetch_video_metadata(url: str) -> Dict[str, Any]:
    """
    Fetch video metadata without downloading.
    Returns thumbnail, title, duration, uploader, and other metadata.
    """
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
        'skip_download': True,  # Don't download the actual video
    }

    results = {
        'success': False,
        'videos': [],
        'errors': []
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            if info is None:
                results['errors'].append('Could not retrieve video information')
                return results

            # Handle playlists
            if 'entries' in info:
                for entry in info['entries']:
                    if entry is None:
                        continue

                    thumbnail_url = None
                    if entry.get('thumbnails'):
                        thumbnail_url = entry['thumbnails'][-1]['url']
                    elif entry.get('thumbnail'):
                        thumbnail_url = entry['thumbnail']

                    results['videos'].append({
                        'title': entry.get('title', 'Untitled'),
                        'duration': entry.get('duration', 0),
                        'thumbnail_url': thumbnail_url,
                        'uploader': entry.get('uploader', 'Unknown'),
                        'view_count': entry.get('view_count', 0),
                        'upload_date': entry.get('upload_date'),
                        'description': entry.get('description', '')[:200] if entry.get('description') else '',
                        'webpage_url': entry.get('webpage_url', url)
                    })
            else:
                # Single video
                thumbnail_url = None
                if info.get('thumbnails'):
                    thumbnail_url = info['thumbnails'][-1]['url']
                elif info.get('thumbnail'):
                    thumbnail_url = info['thumbnail']

                results['videos'].append({
                    'title': info.get('title', 'Untitled'),
                    'duration': info.get('duration', 0),
                    'thumbnail_url': thumbnail_url,
                    'uploader': info.get('uploader', 'Unknown'),
                    'view_count': info.get('view_count', 0),
                    'upload_date': info.get('upload_date'),
                    'description': info.get('description', '')[:200] if info.get('description') else '',
                    'webpage_url': info.get('webpage_url', url)
                })

            results['success'] = True
            results['is_playlist'] = 'entries' in info
            results['playlist_title'] = info.get('title') if 'entries' in info else None

    except Exception as e:
        results['errors'].append(str(e))

    return results

def download_and_process(url: str, output_dir: str, **kwargs) -> Dict[str, Any]:
    # Get the absolute path to ffmpeg
    current_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    ffmpeg_dir = os.path.join(current_dir, 'ffmpeg')
    ffmpeg_path = os.path.join(ffmpeg_dir, 'ffmpeg.exe')

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    print(f"Output directory: {output_dir}")
    print(f"FFmpeg directory: {ffmpeg_dir}")
    print(f"FFmpeg path: {ffmpeg_path}")
    print(f"FFmpeg exists: {os.path.exists(ffmpeg_path)}")

    # Configure yt-dlp options with better error handling
    ydl_opts = {
        # Use flexible format selection that works with most videos
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best',
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'quiet': False,  # Enable verbose output for debugging
        'no_warnings': False,  # Show warnings for debugging
        'ignoreerrors': False,  # Don't ignore errors - we want to see them
        'extract_flat': False,  # Don't extract playlist info only
        'skip_unavailable_fragments': True,
        'writeinfojson': True,  # Write video info to JSON file for debugging
        'geo_bypass': True,  # Recommended for improved reliability/availability
        'writethumbnail': True,  # Download thumbnail
        'merge_output_format': 'mp4',  # Ensure merged files are mp4
        'progress_hooks': kwargs.get('progress_hooks', []),  # CRITICAL: Add progress hooks from kwargs
        'overwrites': True,  # Overwrite existing files (forces re-download for testing)
        'nopart': False,  # Use .part files for in-progress downloads
    }

    # Set FFmpeg location - yt-dlp needs the directory
    if os.path.exists(ffmpeg_path):
        ydl_opts['ffmpeg_location'] = ffmpeg_dir
        # Also try setting as postprocessor args
        ydl_opts['postprocessor_args'] = {
            'ffmpeg': ['-loglevel', 'warning']
        }
        print("FFmpeg found, using custom location")
    else:
        print("FFmpeg not found at custom location, using system PATH")

    # Handle format preference
    format_pref = kwargs.get('format', 'mp4')
    quality = kwargs.get('quality', 'best')

    # Video formats
    if format_pref == 'mp4':
        ydl_opts['merge_output_format'] = 'mp4'
        if quality == 'best':
            ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best'
        elif quality == '1080p':
            ydl_opts['format'] = 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=1080]+bestaudio/best[height<=1080]'
        elif quality == '720p':
            ydl_opts['format'] = 'bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=720]+bestaudio/best[height<=720]'
        elif quality == '480p':
            ydl_opts['format'] = 'bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=480]+bestaudio/best[height<=480]'

    elif format_pref == 'mkv':
        ydl_opts['merge_output_format'] = 'mkv'
        if quality == 'best':
            ydl_opts['format'] = 'bestvideo+bestaudio/best'
        elif quality == '1080p':
            ydl_opts['format'] = 'bestvideo[height<=1080]+bestaudio/best[height<=1080]'
        elif quality == '720p':
            ydl_opts['format'] = 'bestvideo[height<=720]+bestaudio/best[height<=720]'
        elif quality == '480p':
            ydl_opts['format'] = 'bestvideo[height<=480]+bestaudio/best[height<=480]'

    elif format_pref == 'avi':
        ydl_opts['merge_output_format'] = 'avi'
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'avi',
        }]
        if quality == 'best':
            ydl_opts['format'] = 'bestvideo+bestaudio/best'
        elif quality == '1080p':
            ydl_opts['format'] = 'bestvideo[height<=1080]+bestaudio/best[height<=1080]'
        elif quality == '720p':
            ydl_opts['format'] = 'bestvideo[height<=720]+bestaudio/best[height<=720]'
        elif quality == '480p':
            ydl_opts['format'] = 'bestvideo[height<=480]+bestaudio/best[height<=480]'

    elif format_pref == 'webm':
        ydl_opts['merge_output_format'] = 'webm'
        if quality == 'best':
            ydl_opts['format'] = 'bestvideo[ext=webm]+bestaudio[ext=webm]/bestvideo+bestaudio/best'
        elif quality == '1080p':
            ydl_opts['format'] = 'bestvideo[height<=1080][ext=webm]+bestaudio[ext=webm]/bestvideo[height<=1080]+bestaudio/best[height<=1080]'
        elif quality == '720p':
            ydl_opts['format'] = 'bestvideo[height<=720][ext=webm]+bestaudio[ext=webm]/bestvideo[height<=720]+bestaudio/best[height<=720]'
        elif quality == '480p':
            ydl_opts['format'] = 'bestvideo[height<=480][ext=webm]+bestaudio[ext=webm]/bestvideo[height<=480]+bestaudio/best[height<=480]'

    # Audio formats
    elif format_pref == 'mp3':
        # Get bitrate from quality parameter (320, 256, 192, 128)
        bitrate = quality if quality in ['320', '256', '192', '128'] else '192'
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': bitrate,
            }]
        })

    elif format_pref == 'aac':
        bitrate = quality if quality in ['320', '256', '192', '128'] else '192'
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'aac',
                'preferredquality': bitrate,
            }]
        })

    elif format_pref == 'wav':
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
            }]
        })

    # Handle subtitles
    if kwargs.get('subtitles', False):
        subtitle_lang = kwargs.get('subtitle_language', 'en')
        subtitle_format = kwargs.get('subtitle_format', 'srt')

        ydl_opts.update({
            'writesubtitles': True,
            'subtitleslangs': [subtitle_lang],
            'subtitlesformat': subtitle_format,
        })

        # Auto-translate if requested
        if kwargs.get('subtitle_translate', False):
            ydl_opts['writeautomaticsub'] = True

    # Handle time range (download specific section)
    time_range = kwargs.get('time_range', {})
    if time_range and (time_range.get('start') or time_range.get('end')):
        start_time = time_range.get('start', '00:00:00')
        end_time = time_range.get('end', '')

        # Convert HH:MM:SS to seconds
        def time_to_seconds(time_str):
            if not time_str:
                return None
            parts = time_str.split(':')
            if len(parts) == 3:
                h, m, s = parts
                return int(h) * 3600 + int(m) * 60 + int(s)
            elif len(parts) == 2:
                m, s = parts
                return int(m) * 60 + int(s)
            return int(parts[0])

        start_sec = time_to_seconds(start_time) if start_time else None
        end_sec = time_to_seconds(end_time) if end_time else None

        # Add postprocessor for time range extraction
        if 'postprocessors' not in ydl_opts:
            ydl_opts['postprocessors'] = []

        ydl_opts['postprocessors'].insert(0, {
            'key': 'FFmpegVideoRemuxer',
            'preferedformat': format_pref,
        })

        # Use download_ranges for yt-dlp
        if start_sec is not None or end_sec is not None:
            # Ensure FFmpeg is available for time range downloads
            if not os.path.exists(ffmpeg_path):
                print("Warning: FFmpeg required for time range downloads")
            else:
                ydl_opts['download_ranges'] = lambda info, *_: [{
                    'start_time': start_sec,
                    'end_time': end_sec,
                }]
                print(f"Time range: {start_time} to {end_time} ({start_sec}s to {end_sec}s)")

    # Handle network settings
    network_settings = kwargs.get('network_settings', {})
    if network_settings:
        # Concurrent connections (fragments)
        concurrent = int(network_settings.get('concurrent', 1))
        if concurrent > 1:
            ydl_opts['concurrent_fragment_downloads'] = concurrent
            print(f"Concurrent fragment downloads: {concurrent}")

        # Segment size (http_chunk_size)
        segment_size = network_settings.get('segment_size')
        if segment_size:
            # Convert MB to bytes
            chunk_size = int(segment_size) * 1024 * 1024
            ydl_opts['http_chunk_size'] = chunk_size
            print(f"HTTP chunk size: {segment_size}MB ({chunk_size} bytes)")

    results = {
        'success': False,  # Start as False, set to True only if successful
        'downloads': [],
        'errors': [],
        'skipped': []
    }

    try:
        print(f"Starting download for URL: {url}")
        print(f"yt-dlp options: {ydl_opts}")
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # First, extract info to check what we're dealing with
            try:
                print("STARTING DOWNLOAD WITH PROGRESS HOOKS ENABLED...")
                # CRITICAL FIX: Use download=True in single call so hooks fire!
                info = ydl.extract_info(url, download=True)
                
                if info is None:
                    raise Exception("Could not retrieve video information")

                print(f"Video info extracted successfully:")
                print(f"  Title: {info.get('title', 'Unknown')}")
                print(f"  Duration: {info.get('duration', 'Unknown')} seconds")
                print(f"  Uploader: {info.get('uploader', 'Unknown')}")

                # Handle both single videos and playlists
                if 'entries' in info:
                    # This is a playlist - already downloaded via extract_info above!
                    print(f"SUCCESS: Playlist detected: {info.get('title', 'Untitled Playlist')}")
                    entries = list(info['entries'])
                    total_videos = len(entries)

                    for index, entry in enumerate(entries, 1):
                        if entry is None:
                            results['skipped'].append({
                                'index': index,
                                'reason': 'Video information could not be retrieved'
                            })
                            continue

                        # --- THUMBNAIL EXTRACTION FOR PLAYLIST ENTRY ---
                        thumbnail_url = None
                        if entry.get('thumbnails'):
                            thumbnail_url = entry['thumbnails'][-1]['url']
                        elif entry.get('thumbnail'):
                            thumbnail_url = entry['thumbnail']
                        # ---------------------------------------------

                        print(f"SUCCESS: Processed video {index}/{total_videos}: {entry.get('title', 'Untitled')}")

                        results['downloads'].append({
                            'title': entry.get('title', 'Untitled'),
                            'format': format_pref,
                            'quality': quality,
                            'index': index,
                            'duration': entry.get('duration'),
                            'status': 'completed',
                            'filename': f"{entry.get('title', 'Untitled')}.{format_pref}",
                            'thumbnail_url': thumbnail_url
                        })
                else:
                    # Single video - already downloaded in extract_info call above!
                    print("SUCCESS: Single video download completed!")

                    # --- THUMBNAIL EXTRACTION FOR SINGLE VIDEO ---
                    thumbnail_url = None
                    if info.get('thumbnails'):
                        # Get the URL of the highest resolution thumbnail (usually the last in the list)
                        thumbnail_url = info['thumbnails'][-1]['url']
                    elif info.get('thumbnail'):
                        # Fallback to a single 'thumbnail' key if it exists
                        thumbnail_url = info['thumbnail']
                    # ---------------------------------------------
                    
                    # Check if file was actually created
                    expected_filename = f"{info.get('title', 'Untitled')}.{format_pref}"
                    expected_path = os.path.join(output_dir, expected_filename)
                    
                    print(f"Expected file: {expected_path}")
                    
                    # Look for any files that were created
                    created_files = []
                    for file in os.listdir(output_dir):
                        file_path = os.path.join(output_dir, file)
                        if os.path.isfile(file_path):
                            created_files.append(file)
                    
                    print(f"Files in output directory: {created_files}")

                    # Get file size of the main download
                    file_size = 0
                    if os.path.exists(expected_path):
                        file_size = os.path.getsize(expected_path)
                        print(f"File size: {file_size} bytes ({file_size / 1024 / 1024:.2f} MB)")
                    else:
                        # Try to find the actual video file
                        for file in created_files:
                            if file.endswith(('.mp4', '.mkv', '.avi', '.webm', '.mp3', '.aac', '.wav')):
                                file_path = os.path.join(output_dir, file)
                                file_size = os.path.getsize(file_path)
                                print(f"Found file: {file} ({file_size / 1024 / 1024:.2f} MB)")
                                break

                    results['downloads'].append({
                        'title': info.get('title', 'Untitled'),
                        'format': format_pref,
                        'quality': quality,
                        'duration': info.get('duration'),
                        'status': 'completed',
                        'filename': expected_filename,
                        'actual_files': created_files,
                        'thumbnail_url': thumbnail_url,  # ADDED
                        'size': file_size  # ADDED - file size in bytes
                    })
                    
                # Handle transcription if requested
                if kwargs.get('transcribe', False) and results['downloads']:
                    print("Transcription requested...")
                    from app.utils.transcription import transcribe_audio, is_transcription_available

                    if not is_transcription_available():
                        print("Warning: Transcription not available (Whisper not installed)")
                        results['transcription_warning'] = 'Whisper not installed. Install with: pip install openai-whisper'
                    else:
                        for download in results['downloads']:
                            # Find the actual media file
                            filename = download.get('filename')
                            if filename:
                                file_path = os.path.join(output_dir, filename)
                                if os.path.exists(file_path):
                                    print(f"Transcribing: {filename}")
                                    transcript_result = transcribe_audio(file_path, language=kwargs.get('subtitle_language', 'en'))
                                    download['transcription'] = transcript_result
                                else:
                                    print(f"File not found for transcription: {file_path}")

                # Only set success to True if we have downloads and no errors
                if results['downloads'] and not results['errors']:
                    results['success'] = True
                    print("All downloads completed successfully!")
                    
            except yt_dlp.utils.DownloadError as e:
                error_msg = str(e)
                print(f"yt-dlp DownloadError: {error_msg}")
                
                if "blocked it in your country" in error_msg:
                    results['errors'].append({
                        'error': 'Video is blocked in your country',
                        'details': error_msg
                    })
                elif "Content not available" in error_msg or "Video unavailable" in error_msg:
                    results['errors'].append({
                        'error': 'Video is no longer available',
                        'details': error_msg
                    })
                elif "Sign in to confirm your age" in error_msg:
                    results['errors'].append({
                        'error': 'Age-restricted video',
                        'details': 'This video requires sign-in to confirm age'
                    })
                else:
                    results['errors'].append({
                        'error': 'Download failed',
                        'details': error_msg
                    })
                
    except Exception as e:
        error_msg = str(e)
        print(f"Unexpected error: {error_msg}")
        results['errors'].append({
            'error': 'Process failed',
            'details': error_msg
        })

    # Add summary to results
    results['summary'] = {
        'total_attempted': len(results['downloads']) + len(results['errors']) + len(results['skipped']),
        'successful': len(results['downloads']),
        'failed': len(results['errors']),
        'skipped': len(results['skipped'])
    }

    print(f"Final results: {results}")
    return results