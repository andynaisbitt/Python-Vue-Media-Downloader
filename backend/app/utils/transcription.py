"""
Audio Transcription Module
Provides transcription services for downloaded audio/video files
"""
import os
import subprocess
import json
from typing import Dict, Any, Optional

def transcribe_audio(audio_file_path: str, language: str = 'en') -> Dict[str, Any]:
    """
    Transcribe audio file to text

    This function attempts to use Whisper (OpenAI's speech recognition model)
    if available, otherwise falls back to a simple placeholder.

    Args:
        audio_file_path: Path to the audio/video file
        language: Language code (e.g., 'en', 'es', 'fr')

    Returns:
        Dict with transcription result
    """

    if not os.path.exists(audio_file_path):
        return {
            'success': False,
            'error': 'Audio file not found',
            'file': audio_file_path
        }

    print(f"Attempting transcription of: {audio_file_path}")

    # Try to use Whisper if installed
    try:
        import whisper

        print("Loading Whisper model...")
        # Use base model for balance of speed and accuracy
        # Options: tiny, base, small, medium, large
        model = whisper.load_model("base")

        print("Transcribing audio...")
        result = model.transcribe(
            audio_file_path,
            language=language if language != 'auto' else None,
            fp16=False  # Disable FP16 for CPU compatibility
        )

        # Save transcription to text file
        transcript_path = audio_file_path.rsplit('.', 1)[0] + '.transcript.txt'
        with open(transcript_path, 'w', encoding='utf-8') as f:
            f.write(result['text'])

        # Save full result with timestamps to JSON
        transcript_json_path = audio_file_path.rsplit('.', 1)[0] + '.transcript.json'
        with open(transcript_json_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        print(f"Transcription saved to: {transcript_path}")

        return {
            'success': True,
            'text': result['text'],
            'language': result.get('language'),
            'segments': len(result.get('segments', [])),
            'transcript_file': transcript_path,
            'transcript_json': transcript_json_path
        }

    except ImportError:
        # Whisper not installed
        print("Whisper not installed. Install with: pip install openai-whisper")

        # Try to use ffmpeg to extract text if available (won't work, but shows intent)
        return {
            'success': False,
            'error': 'Whisper not installed',
            'message': 'To enable transcription, install Whisper: pip install openai-whisper',
            'note': 'Whisper requires PyTorch. See: https://github.com/openai/whisper'
        }

    except Exception as e:
        print(f"Transcription error: {e}")
        return {
            'success': False,
            'error': str(e),
            'file': audio_file_path
        }

def is_transcription_available() -> bool:
    """Check if transcription is available (Whisper installed)"""
    try:
        import whisper
        return True
    except ImportError:
        return False

def get_transcription_info() -> Dict[str, Any]:
    """Get information about transcription availability"""
    available = is_transcription_available()

    info = {
        'available': available,
        'provider': 'OpenAI Whisper' if available else None,
    }

    if available:
        try:
            import whisper
            info['models'] = ['tiny', 'base', 'small', 'medium', 'large']
            info['default_model'] = 'base'
            info['languages'] = 'auto-detect or specify'
        except:
            pass
    else:
        info['install_command'] = 'pip install openai-whisper'
        info['note'] = 'Requires PyTorch'

    return info
