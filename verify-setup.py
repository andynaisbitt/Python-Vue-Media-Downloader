#!/usr/bin/env python3
"""
YouTube Video Downloader - Installation Verification Script
Checks if all required dependencies are properly installed.
"""

import os
import sys
import subprocess
from pathlib import Path

# ANSI color codes for pretty output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
BOLD = '\033[1m'
RESET = '\033[0m'

def print_header(text):
    print(f"\n{BLUE}{BOLD}{'='*60}{RESET}")
    print(f"{BLUE}{BOLD}{text.center(60)}{RESET}")
    print(f"{BLUE}{BOLD}{'='*60}{RESET}\n")

def print_success(text):
    print(f"{GREEN}[OK] {text}{RESET}")

def print_error(text):
    print(f"{RED}[X] {text}{RESET}")

def print_warning(text):
    print(f"{YELLOW}[!] {text}{RESET}")

def check_python_version():
    """Check if Python version is 3.8 or higher"""
    print_header("Checking Python Version")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print_success(f"Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print_error(f"Python {version.major}.{version.minor}.{version.micro} (requires 3.8+)")
        return False

def check_node():
    """Check if Node.js is installed"""
    print_header("Checking Node.js")
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.strip()
            print_success(f"Node.js {version}")
            return True
    except FileNotFoundError:
        print_error("Node.js not found")
        print_warning("Download from: https://nodejs.org/")
        return False

def check_npm():
    """Check if npm is installed"""
    try:
        result = subprocess.run(['npm', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.strip()
            print_success(f"npm {version}")
            return True
    except FileNotFoundError:
        print_error("npm not found")
        return False

def check_ffmpeg():
    """Check if FFmpeg is installed"""
    print_header("Checking FFmpeg")

    # Check local ffmpeg folder
    backend_dir = Path(__file__).parent / 'backend'
    ffmpeg_dir = backend_dir / 'ffmpeg'

    # Check for platform-specific executable
    if sys.platform == 'win32':
        ffmpeg_local = ffmpeg_dir / 'ffmpeg.exe'
        ffprobe_local = ffmpeg_dir / 'ffprobe.exe'
    else:
        ffmpeg_local = ffmpeg_dir / 'ffmpeg'
        ffprobe_local = ffmpeg_dir / 'ffprobe'

    # Check local installation
    if ffmpeg_local.exists() and ffprobe_local.exists():
        print_success(f"FFmpeg found in: {ffmpeg_dir}")
        print_success(f"  - ffmpeg: {ffmpeg_local.name}")
        print_success(f"  - ffprobe: {ffprobe_local.name}")
        return True

    # Check system-wide installation
    try:
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print_success(f"FFmpeg (system-wide): {version_line}")
            print_warning("Consider installing FFmpeg locally in backend/ffmpeg/ for portability")
            return True
    except FileNotFoundError:
        pass

    # FFmpeg not found
    print_error("FFmpeg not found!")
    print_warning("FFmpeg is REQUIRED for video/audio processing.")
    print_warning("\nInstallation options:")
    print_warning("1. Local (recommended): Download to backend/ffmpeg/")
    if sys.platform == 'win32':
        print_warning("   Windows: https://www.gyan.dev/ffmpeg/builds/")
    elif sys.platform == 'darwin':
        print_warning("   macOS: https://evermeet.cx/ffmpeg/")
    else:
        print_warning("   Linux: sudo apt install ffmpeg")
    print_warning("\n2. System-wide: See backend/ffmpeg/README.md")
    return False

def check_python_packages():
    """Check if required Python packages are installed"""
    print_header("Checking Python Packages")

    required_packages = [
        'flask',
        'yt_dlp',
        'flask_cors'
    ]

    all_installed = True
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print_success(f"{package}")
        except ImportError:
            print_error(f"{package} not installed")
            all_installed = False

    if not all_installed:
        print_warning("\nInstall missing packages:")
        print_warning("cd backend && pip install -r requirements.txt")

    return all_installed

def check_frontend_packages():
    """Check if frontend node_modules exist"""
    print_header("Checking Frontend Packages")

    node_modules = Path(__file__).parent / 'frontend' / 'node_modules'

    if node_modules.exists():
        print_success("node_modules/ exists")
        return True
    else:
        print_error("node_modules/ not found")
        print_warning("Install frontend dependencies:")
        print_warning("cd frontend && npm install")
        return False

def check_directories():
    """Check if required directories exist"""
    print_header("Checking Directory Structure")

    base_dir = Path(__file__).parent
    required_dirs = [
        base_dir / 'backend',
        base_dir / 'frontend',
        base_dir / 'backend' / 'app',
        base_dir / 'frontend' / 'src',
        base_dir / 'backend' / 'ffmpeg'
    ]

    all_exist = True
    for directory in required_dirs:
        if directory.exists():
            print_success(f"{directory.name}/")
        else:
            print_error(f"{directory.name}/ not found")
            all_exist = False

    return all_exist

def main():
    """Run all verification checks"""
    print(f"{BOLD}")
    print("=" * 62)
    print("     YouTube Video Downloader - Setup Verification")
    print("                   Version 1.0.0")
    print("=" * 62)
    print(f"{RESET}")

    checks = [
        ("Python Version", check_python_version),
        ("Node.js", check_node),
        ("npm", check_npm),
        ("FFmpeg", check_ffmpeg),
        ("Python Packages", check_python_packages),
        ("Frontend Packages", check_frontend_packages),
        ("Directory Structure", check_directories)
    ]

    results = []
    for name, check_func in checks:
        result = check_func()
        results.append((name, result))

    # Summary
    print_header("Verification Summary")

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = f"{GREEN}PASS{RESET}" if result else f"{RED}FAIL{RESET}"
        print(f"{name:.<30} {status}")

    print(f"\n{BOLD}Score: {passed}/{total} checks passed{RESET}")

    if passed == total:
        print(f"\n{GREEN}{BOLD}[OK] All checks passed! You're ready to run the app.{RESET}")
        print(f"\n{BOLD}Next steps:{RESET}")
        print("1. Backend: cd backend && python run.py")
        print("2. Frontend: cd frontend && npm run dev")
        print("3. Open: http://localhost:5173")
        return 0
    else:
        print(f"\n{RED}{BOLD}[X] Some checks failed. Please fix the issues above.{RESET}")
        print(f"\n{BOLD}Quick fixes:{RESET}")
        print("• Python packages: cd backend && pip install -r requirements.txt")
        print("• Frontend packages: cd frontend && npm install")
        print("• FFmpeg: See backend/ffmpeg/README.md")
        return 1

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}Verification cancelled by user.{RESET}")
        sys.exit(1)
