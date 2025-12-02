"""Quick test of the download functionality with the fixed format strings"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.utils.downloader import download_and_process
import json

# Use a very short video for quick testing
TEST_URL = 'https://www.youtube.com/watch?v=jNQXAC9IVRw'  # 19 seconds - "Me at the zoo"

def main():
    print("\n" + "="*80)
    print("QUICK DOWNLOAD TEST")
    print("="*80)
    print(f"URL: {TEST_URL}")
    print(f"Format: MP4, Quality: best")
    print("="*80 + "\n")

    output_dir = os.path.join(os.path.dirname(__file__), 'downloads', 'test')
    os.makedirs(output_dir, exist_ok=True)

    try:
        result = download_and_process(
            url=TEST_URL,
            output_dir=output_dir,
            format='mp4',
            quality='best'
        )

        print(f"\n{'='*80}")
        print("RESULT")
        print(f"{'='*80}")
        print(json.dumps(result, indent=2))

        if result['success']:
            print(f"\n✅ SUCCESS - Download completed!")
            if result['downloads']:
                dl = result['downloads'][0]
                print(f"   Title: {dl['title']}")
                print(f"   Filename: {dl['filename']}")
                print(f"   Thumbnail URL: {dl.get('thumbnail_url', 'N/A')[:80]}...")
            return True
        else:
            print(f"\n❌ FAILED")
            for error in result.get('errors', []):
                print(f"   Error: {error.get('error')}")
                print(f"   Details: {error.get('details', '')[:200]}")
            return False

    except Exception as e:
        print(f"\n❌ EXCEPTION: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = main()
    print(f"\n{'='*80}\n")
    sys.exit(0 if success else 1)
