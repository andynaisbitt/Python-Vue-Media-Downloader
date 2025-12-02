# backend/app/api/routes.py
from flask import jsonify, request, current_app, send_file
from app.api import bp
from app.api.download_manager import create_job, get_job_status
from app.utils.downloader import fetch_video_metadata
import os

@bp.route('/metadata', methods=['POST'])
def get_video_metadata():
    """Fetch video metadata without downloading"""
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({'error': 'No URL provided'}), 400

    url = data.get('url')

    try:
        metadata = fetch_video_metadata(url)
        return jsonify(metadata), 200
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500

@bp.route('/download', methods=['POST'])
def start_download():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({'error': 'No URL provided'}), 400

    url = data.get('url')

    # Get advanced options if provided
    advanced_opts = data.get('advancedOptions', {})

    # Consolidate all options to pass to the download manager
    options = {
        'output_dir': current_app.config['UPLOAD_FOLDER'],
        'format': data.get('format', 'mp4'),
        'quality': data.get('quality', 'best'),

        # Basic subtitle options
        'subtitles': data.get('subtitles', False),
        'transcribe': data.get('transcribe', False),

        # Advanced subtitle options
        'subtitle_language': advanced_opts.get('subtitleOptions', {}).get('language', 'en'),
        'subtitle_format': advanced_opts.get('subtitleOptions', {}).get('format', 'srt'),
        'subtitle_translate': advanced_opts.get('subtitleOptions', {}).get('translate', False),

        # Time range options
        'time_range': advanced_opts.get('timeRange', {}),

        # Network settings
        'network_settings': advanced_opts.get('networkSettings', {}),
    }

    try:
        job_id = create_job(url, options)
        return jsonify({'job_id': job_id}), 202
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/download/status/<job_id>')
def get_download_status_route(job_id):
    status = get_job_status(job_id)
    if status:
        return jsonify(status)
    else:
        return jsonify({'error': 'Job not found'}), 404

@bp.route('/download/file/<path:filename>')
def download_file(filename):
    try:
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return jsonify({'error': 'File not found'}), 404

@bp.route('/download/thumbnail/<path:filename>')
def get_thumbnail(filename):
    try:
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        return send_file(file_path, mimetype='image/jpeg')
    except Exception as e:
        return jsonify({'error': 'Thumbnail not found'}), 404