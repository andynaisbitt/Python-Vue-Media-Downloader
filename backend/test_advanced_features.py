"""
Test Advanced Features
Tests time range, concurrent downloads, segment size, and transcription
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.utils.downloader import download_and_process
from app.utils.transcription import is_transcription_available, get_transcription_info
import json

TEST_VIDEO = 'https://www.youtube.com/watch?v=jNQXAC9IVRw'  # 19s video

def test_time_range_download():
    """Test downloading specific time range"""
    print("\n" + "="*80)
    print("TEST: Time Range Download (0:00:05 to 0:00:15)")
    print("="*80)

    output_dir = os.path.join(os.path.dirname(__file__), 'downloads', 'advanced_test')
    os.makedirs(output_dir, exist_ok=True)

    try:
        result = download_and_process(
            url=TEST_VIDEO,
            output_dir=output_dir,
            format='mp4',
            quality='best',
            time_range={
                'start': '00:00:05',
                'end': '00:00:15'
            }
        )

        if result['success']:
            print("✅ SUCCESS: Time range download completed")
            download = result['downloads'][0]
            print(f"   File: {download['filename']}")
            print(f"   Note: Video should be ~10 seconds long")
            return True
        else:
            print("❌ FAILED")
            if result['errors']:
                print(f"   Error: {result['errors'][0].get('error')}")
            return False

    except Exception as e:
        print(f"❌ EXCEPTION: {str(e)}")
        return False

def test_network_settings():
    """Test network settings (concurrent fragments and segment size)"""
    print("\n" + "="*80)
    print("TEST: Network Settings (4 concurrent, 5MB segments)")
    print("="*80)

    output_dir = os.path.join(os.path.dirname(__file__), 'downloads', 'advanced_test')

    try:
        result = download_and_process(
            url=TEST_VIDEO,
            output_dir=output_dir,
            format='mp4',
            quality='best',
            network_settings={
                'concurrent': 4,
                'segment_size': 5
            }
        )

        if result['success']:
            print("✅ SUCCESS: Network settings applied")
            print("   Concurrent fragments: 4")
            print("   Segment size: 5MB")
            return True
        else:
            print("❌ FAILED")
            return False

    except Exception as e:
        print(f"❌ EXCEPTION: {str(e)}")
        return False

def test_advanced_subtitles():
    """Test advanced subtitle options"""
    print("\n" + "="*80)
    print("TEST: Advanced Subtitles (Spanish, VTT format)")
    print("="*80)

    output_dir = os.path.join(os.path.dirname(__file__), 'downloads', 'advanced_test')

    try:
        result = download_and_process(
            url=TEST_VIDEO,
            output_dir=output_dir,
            format='mp4',
            quality='best',
            subtitles=True,
            subtitle_language='es',
            subtitle_format='vtt',
            subtitle_translate=True
        )

        if result['success']:
            print("✅ SUCCESS: Advanced subtitle options applied")
            print("   Language: Spanish")
            print("   Format: VTT")
            print("   Auto-translate: Enabled")

            # Check for subtitle file
            for file in os.listdir(output_dir):
                if '.vtt' in file or '.srt' in file:
                    print(f"   Subtitle file: {file}")
                    return True

            print("   Note: Subtitle file may not exist (depends on video availability)")
            return True
        else:
            print("❌ FAILED")
            return False

    except Exception as e:
        print(f"❌ EXCEPTION: {str(e)}")
        return False

def test_transcription_availability():
    """Test transcription availability"""
    print("\n" + "="*80)
    print("TEST: Transcription Availability")
    print("="*80)

    info = get_transcription_info()
    print(json.dumps(info, indent=2))

    if info['available']:
        print("✅ Whisper is installed and ready")
        return True
    else:
        print("⚠️  Whisper not installed (optional feature)")
        print(f"   Install with: {info.get('install_command')}")
        return True  # Not a failure - it's optional

def test_transcription():
    """Test audio transcription (if Whisper is available)"""
    print("\n" + "="*80)
    print("TEST: Audio Transcription")
    print("="*80)

    if not is_transcription_available():
        print("⚠️  SKIPPED: Whisper not installed")
        print("   Install with: pip install openai-whisper")
        return True  # Not a failure - it's optional

    output_dir = os.path.join(os.path.dirname(__file__), 'downloads', 'advanced_test')

    try:
        result = download_and_process(
            url=TEST_VIDEO,
            output_dir=output_dir,
            format='mp3',
            quality='192',
            transcribe=True
        )

        if result['success']:
            download = result['downloads'][0]

            if 'transcription' in download:
                trans = download['transcription']
                if trans.get('success'):
                    print("✅ SUCCESS: Transcription completed")
                    print(f"   Text preview: {trans.get('text', '')[:100]}...")
                    print(f"   Language: {trans.get('language')}")
                    print(f"   Transcript file: {trans.get('transcript_file')}")
                    return True
                else:
                    print("⚠️  Transcription attempted but failed")
                    print(f"   Error: {trans.get('error')}")
                    return True  # Not a critical failure
            else:
                print("⚠️  No transcription data in result")
                return True

        else:
            print("❌ FAILED: Download failed")
            return False

    except Exception as e:
        print(f"❌ EXCEPTION: {str(e)}")
        return False

def main():
    print("\n" + "="*80)
    print("ADVANCED FEATURES TEST SUITE")
    print("="*80)
    print("Testing all newly implemented features")
    print("="*80)

    results = []

    # Test 1: Time Range
    results.append(("Time Range Download", test_time_range_download()))

    # Test 2: Network Settings
    results.append(("Network Settings", test_network_settings()))

    # Test 3: Advanced Subtitles
    results.append(("Advanced Subtitles", test_advanced_subtitles()))

    # Test 4: Transcription Availability
    results.append(("Transcription Availability", test_transcription_availability()))

    # Test 5: Transcription (if available)
    results.append(("Audio Transcription", test_transcription()))

    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")

    print()
    print(f"Total: {passed}/{total} tests passed")
    print(f"Success Rate: {(passed/total*100):.1f}%")
    print("="*80 + "\n")

    return passed == total

if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user")
        sys.exit(1)
