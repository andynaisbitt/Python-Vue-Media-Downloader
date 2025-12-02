"""
COMPREHENSIVE TEST SUITE FOR YOUTUBE DOWNLOADER
Tests all features, formats, qualities, and edge cases
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.utils.downloader import download_and_process
import json
import time

# Short test videos to minimize test time
TEST_VIDEOS = {
    'short': 'https://www.youtube.com/watch?v=jNQXAC9IVRw',  # 19s - "Me at the zoo"
    'medium': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',  # ~3m - Rick Roll (iconic)
}

class TestResults:
    def __init__(self):
        self.total = 0
        self.passed = 0
        self.failed = 0
        self.skipped = 0
        self.tests = []

    def add_result(self, name, status, details="", error=None):
        self.total += 1
        if status == "PASS":
            self.passed += 1
        elif status == "FAIL":
            self.failed += 1
        elif status == "SKIP":
            self.skipped += 1

        self.tests.append({
            'name': name,
            'status': status,
            'details': details,
            'error': error
        })

    def print_summary(self):
        print("\n" + "="*80)
        print("COMPREHENSIVE TEST SUMMARY")
        print("="*80)
        print(f"Total Tests:    {self.total}")
        print(f"PASSED:  {self.passed}")
        print(f"FAILED:  {self.failed}")
        print(f"SKIPPED: {self.skipped}")
        print(f"Success Rate:   {(self.passed/self.total*100):.1f}%")
        print("="*80 + "\n")

        # Print failed tests
        if self.failed > 0:
            print("FAILED TESTS:")
            print("-"*80)
            for test in self.tests:
                if test['status'] == "FAIL":
                    print(f"  X {test['name']}")
                    if test['error']:
                        print(f"    Error: {test['error'][:100]}")
            print()

results = TestResults()

def test_download(name, url, format_type, quality, **kwargs):
    """Generic test function for downloads"""
    print(f"\n[TEST] {name}")
    print(f"  URL: {url}")
    print(f"  Format: {format_type}, Quality: {quality}")
    if kwargs:
        print(f"  Options: {kwargs}")

    output_dir = os.path.join(os.path.dirname(__file__), 'downloads', 'comprehensive_test')
    os.makedirs(output_dir, exist_ok=True)

    try:
        result = download_and_process(
            url=url,
            output_dir=output_dir,
            format=format_type,
            quality=quality,
            **kwargs
        )

        if result['success']:
            download = result['downloads'][0]
            details = f"Title: {download['title']}, File: {download['filename']}"
            if download.get('thumbnail_url'):
                details += f", Thumbnail: YES"
            print(f"  [PASS] {details}")
            results.add_result(name, "PASS", details)
            return True
        else:
            error = result['errors'][0] if result['errors'] else {'error': 'Unknown error'}
            error_msg = f"{error.get('error')}: {error.get('details', '')[:100]}"
            print(f"  [FAIL] {error_msg}")
            results.add_result(name, "FAIL", error=error_msg)
            return False

    except Exception as e:
        error_msg = str(e)[:200]
        print(f"  [FAIL] Exception: {error_msg}")
        results.add_result(name, "FAIL", error=error_msg)
        return False

def test_api_connectivity():
    """Test if backend API is accessible"""
    print("\n" + "="*80)
    print("PHASE 1: API CONNECTIVITY")
    print("="*80)

    import requests
    try:
        response = requests.get('http://localhost:5000/', timeout=5)
        print("  [PASS] Backend API is accessible")
        results.add_result("API Connectivity", "PASS", "Backend responding")
        return True
    except Exception as e:
        print(f"  [FAIL] Cannot reach backend: {e}")
        results.add_result("API Connectivity", "FAIL", error=str(e))
        return False

def test_video_formats():
    """Test all video format combinations"""
    print("\n" + "="*80)
    print("PHASE 2: VIDEO FORMAT TESTS")
    print("="*80)

    # MP4 Tests
    test_download("MP4 - Best Quality", TEST_VIDEOS['short'], 'mp4', 'best')
    test_download("MP4 - 1080p", TEST_VIDEOS['short'], 'mp4', '1080p')
    test_download("MP4 - 720p", TEST_VIDEOS['short'], 'mp4', '720p')
    test_download("MP4 - 480p", TEST_VIDEOS['short'], 'mp4', '480p')

    # WebM Tests (if supported)
    test_download("WebM - Best Quality", TEST_VIDEOS['short'], 'webm', 'best')

def test_audio_formats():
    """Test all audio format combinations"""
    print("\n" + "="*80)
    print("PHASE 3: AUDIO FORMAT TESTS")
    print("="*80)

    # MP3 Tests
    test_download("MP3 - Audio Only", TEST_VIDEOS['short'], 'mp3', 'best')

def test_subtitle_features():
    """Test subtitle download functionality"""
    print("\n" + "="*80)
    print("PHASE 4: SUBTITLE TESTS")
    print("="*80)

    # Test with subtitles enabled
    test_download("MP4 with Subtitles", TEST_VIDEOS['short'], 'mp4', 'best', subtitles=True)

def test_thumbnail_downloads():
    """Verify thumbnails are downloaded"""
    print("\n" + "="*80)
    print("PHASE 5: THUMBNAIL VERIFICATION")
    print("="*80)

    output_dir = os.path.join(os.path.dirname(__file__), 'downloads', 'comprehensive_test')

    # Check if thumbnail files exist
    thumbnail_found = False
    for file in os.listdir(output_dir):
        if file.endswith('.webp') or file.endswith('.jpg') or file.endswith('.png'):
            thumbnail_found = True
            print(f"  [PASS] Thumbnail found: {file}")
            break

    if thumbnail_found:
        results.add_result("Thumbnail Download", "PASS", "Thumbnails present")
    else:
        print("  [FAIL] No thumbnails found")
        results.add_result("Thumbnail Download", "FAIL", error="No thumbnail files")

def test_error_handling():
    """Test error handling with invalid URLs"""
    print("\n" + "="*80)
    print("PHASE 6: ERROR HANDLING TESTS")
    print("="*80)

    # Invalid URL
    print("\n[TEST] Invalid URL Handling")
    output_dir = os.path.join(os.path.dirname(__file__), 'downloads', 'comprehensive_test')

    try:
        result = download_and_process(
            url='https://www.youtube.com/watch?v=INVALID_VIDEO_ID',
            output_dir=output_dir,
            format='mp4',
            quality='best'
        )

        if not result['success'] and result['errors']:
            print("  [PASS] Invalid URL properly rejected")
            results.add_result("Error Handling - Invalid URL", "PASS", "Errors properly returned")
        else:
            print("  [FAIL] Invalid URL was not rejected")
            results.add_result("Error Handling - Invalid URL", "FAIL", error="Should have failed")
    except Exception as e:
        print(f"  [PASS] Exception properly raised: {str(e)[:50]}")
        results.add_result("Error Handling - Invalid URL", "PASS", "Exception raised")

def test_metadata_files():
    """Verify metadata JSON files are created"""
    print("\n" + "="*80)
    print("PHASE 7: METADATA VERIFICATION")
    print("="*80)

    output_dir = os.path.join(os.path.dirname(__file__), 'downloads', 'comprehensive_test')

    # Check for .info.json files
    json_found = False
    for file in os.listdir(output_dir):
        if file.endswith('.info.json'):
            json_found = True
            file_path = os.path.join(output_dir, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if 'title' in data and 'duration' in data:
                        print(f"  [PASS] Valid metadata: {file}")
                        print(f"    Title: {data.get('title')}")
                        print(f"    Duration: {data.get('duration')}s")
                        results.add_result("Metadata Files", "PASS", f"JSON valid: {file}")
                        break
            except Exception as e:
                print(f"  [FAIL] Invalid JSON: {e}")
                results.add_result("Metadata Files", "FAIL", error=str(e))

    if not json_found:
        print("  [FAIL] No metadata JSON files found")
        results.add_result("Metadata Files", "FAIL", error="No JSON files")

def test_file_integrity():
    """Verify downloaded files exist and are not empty"""
    print("\n" + "="*80)
    print("PHASE 8: FILE INTEGRITY CHECKS")
    print("="*80)

    output_dir = os.path.join(os.path.dirname(__file__), 'downloads', 'comprehensive_test')

    video_files = [f for f in os.listdir(output_dir) if f.endswith(('.mp4', '.mp3', '.webm'))]

    if not video_files:
        print("  [FAIL] No video/audio files found")
        results.add_result("File Integrity", "FAIL", error="No media files")
        return

    for file in video_files:
        file_path = os.path.join(output_dir, file)
        file_size = os.path.getsize(file_path)

        if file_size > 0:
            print(f"  [PASS] {file} ({file_size / 1024:.1f} KB)")
            results.add_result(f"File Integrity - {file}", "PASS", f"Size: {file_size / 1024:.1f} KB")
        else:
            print(f"  [FAIL] {file} is empty")
            results.add_result(f"File Integrity - {file}", "FAIL", error="File is 0 bytes")

def main():
    print("\n" + "="*80)
    print("YOUTUBE DOWNLOADER - COMPREHENSIVE TEST SUITE")
    print("="*80)
    print("This will test ALL features and combinations")
    print("Estimated time: 2-5 minutes")
    print("="*80)

    start_time = time.time()

    # Phase 1: Connectivity
    if not test_api_connectivity():
        print("\n[WARNING] Backend not accessible. Skipping API tests.")
        print("Make sure backend is running: python run.py")

    # Phase 2-3: Format Tests
    test_video_formats()
    test_audio_formats()

    # Phase 4: Subtitle Tests
    test_subtitle_features()

    # Phase 5-8: Verification Tests
    test_thumbnail_downloads()
    test_error_handling()
    test_metadata_files()
    test_file_integrity()

    # Summary
    elapsed = time.time() - start_time
    results.print_summary()

    print(f"Total Time: {elapsed:.1f} seconds")
    print("="*80 + "\n")

    # Return success/failure
    return results.failed == 0

if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user")
        results.print_summary()
        sys.exit(1)
