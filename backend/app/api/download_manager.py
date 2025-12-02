# backend/app/api/download_manager.py
import uuid
from threading import Thread, Lock
from app.utils.downloader import download_and_process

# In-memory store for download jobs
# In a production environment, you might use Redis or a database
_jobs = {}
_jobs_lock = Lock()

def create_job(url, options):
    """Creates a new download job and starts it in a background thread."""
    job_id = str(uuid.uuid4())
    
    with _jobs_lock:
        _jobs[job_id] = {
            'job_id': job_id,
            'status': 'queued',
            'progress': 0,
            'url': url,
            'options': options,
            'result': None
        }

    # Start the download in a background thread
    thread = Thread(target=_run_download_job, args=(job_id, url, options))
    thread.daemon = True
    thread.start()
    
    return job_id

def get_job_status(job_id):
    """Retrieves the status of a specific download job."""
    with _jobs_lock:
        job = _jobs.get(job_id)
        if job:
            # Create a copy without non-serializable items (like progress_hooks)
            serializable_job = {
                'job_id': job['job_id'],
                'status': job['status'],
                'progress': job.get('progress', 0),
                'url': job['url'],
                'result': job.get('result'),
                'speed': job.get('speed'),
                'eta': job.get('eta'),
                'downloaded_bytes': job.get('downloaded_bytes'),
                'total_bytes': job.get('total_bytes')
            }
            return serializable_job
        return None

def _run_download_job(job_id, url, options):
    """The target function for the download thread."""
    
    def progress_hook(d):
        """Hook for yt-dlp to report progress."""
        status = d.get('status', 'unknown')
        print(f"HOOK FIRED: {status}")  # DEBUG

        with _jobs_lock:
            job = _jobs[job_id]

            if status == 'downloading':
                job['status'] = 'downloading'

                # Store byte-level information
                downloaded_bytes = d.get('downloaded_bytes', 0)
                total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate')

                # Get filename being downloaded
                filename = d.get('filename', '')
                if filename:
                    job['current_file'] = filename

                job['downloaded_bytes'] = downloaded_bytes
                job['total_bytes'] = total_bytes

                if total_bytes and total_bytes > 0:
                    job['progress'] = round((downloaded_bytes / total_bytes) * 100, 2)
                else:
                    # If no total bytes, show partial progress based on downloaded
                    job['progress'] = min(downloaded_bytes / (1024 * 1024), 99)  # Cap at 99%

                job['speed'] = d.get('speed', 0)
                job['eta'] = d.get('eta', 0)

                # Additional metadata
                job['_percent_str'] = d.get('_percent_str', f"{job['progress']:.1f}%")
                job['_speed_str'] = d.get('_speed_str', 'Unknown')
                job['_eta_str'] = d.get('_eta_str', 'Unknown')

                # DEBUG: Print detailed progress info
                print(f"PROGRESS: {job['progress']:.1f}% | {downloaded_bytes}/{total_bytes} bytes | Speed: {job['speed']} | ETA: {job['eta']}s")

            elif status == 'finished':
                print(f"HOOK: Download finished, starting post-processing")
                job['status'] = 'processing'
                job['progress'] = 100
                job['downloaded_bytes'] = job.get('total_bytes', 0)

            elif status == 'error':
                print(f"HOOK ERROR: {d.get('error', 'Unknown error')}")
                job['status'] = 'error'
                job['error'] = str(d.get('error', 'Download failed'))

    # Add the progress hook to the options
    options['progress_hooks'] = [progress_hook]
    
    with _jobs_lock:
        _jobs[job_id]['status'] = 'starting'

    try:
        # Run the actual download function
        result = download_and_process(url, **options)
        
        # Update the job with the final result
        with _jobs_lock:
            _jobs[job_id]['status'] = 'completed'
            _jobs[job_id]['result'] = result

    except Exception as e:
        with _jobs_lock:
            _jobs[job_id]['status'] = 'error'
            _jobs[job_id]['result'] = {'error': str(e)}

