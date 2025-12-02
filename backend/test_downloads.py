"""
Test script for YouTube downloader functionality
Tests various formats, qualities, and edge cases
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.utils.downloader import download_and_process
import json

# Test URLs - use short videos to speed up testing
TEST_URLS = {
    'short_video': 'https://www.youtube.com/watch?v=jNQXAC9IVRw',  # "Me at the zoo" - first YouTube video
    'popular_video': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',  # Rick Astley
}

def test_download(url, format_type, quality, test_name):
    """Test a single download configuration"""
    print(f"\n{'='*80}")
    print(f"TEST: {test_name}")
    print(f"URL: {url}")
    print(f"Format: {format_type}, Quality: {quality}")
    print(f"{'='*80}\n")

    output_dir = os.path.join(os.path.dirname(__file__), 'downloads', 'test')
    os.makedirs(output_dir, exist_ok=True)

    try:
        result = download_and_process(
            url=url,
            output_dir=output_dir,
            format=format_type,
            quality=quality
        )

        print(f"\n{'='*80}")
        print(f"RESULT: {test_name}")
        print(f"{'='*80}")
        print(json.dumps(result, indent=2))

        # Check success criteria
        if result['success']:
            print(f"✅ SUCCESS")
            if result['downloads']:
                download = result['downloads'][0]
                print(f"   Title: {download['title']}")
                print(f"   Filename: {download['filename']}")
                print(f"   Thumbnail: {download.get('thumbnail_url', 'N/A')}")
                print(f"   Duration: {download.get('duration', 'N/A')}s")
        else:
            print(f"❌ FAILED")
            if result['errors']:
                for error in result['errors']:
                    print(f"   Error: {error.get('error')}")
                    print(f"   Details: {error.get('details', '')[:100]}")

        return result['success']

    except Exception as e:
        print(f"❌ EXCEPTION: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("\n" + "="*80)
    print("YOUTUBE DOWNLOADER TEST SUITE")
    print("="*80)

    results = []

    # Test 1: MP4 Best Quality
    results.append(test_download(
        TEST_URLS['short_video'],
        'mp4',
        'best',
        "MP4 - Best Quality"
    ))

    # Test 2: MP4 720p
    results.append(test_download(
        TEST_URLS['short_video'],
        'mp4',
        '720p',
        "MP4 - 720p Quality"
    ))

    # Test 3: MP3 Audio
    results.append(test_download(
        TEST_URLS['short_video'],
        'mp3',
        'best',
        "MP3 - Audio Only"
    ))

    # Test 4: WebM Format
    results.append(test_download(
        TEST_URLS['short_video'],
        'webm',
        'best',
        "WebM - Best Quality"
    ))

    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    total = len(results)
    passed = sum(results)
    failed = total - passed

    print(f"Total Tests: {total}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"Success Rate: {(passed/total*100):.1f}%")
    print("="*80 + "\n")

    return passed == total

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
