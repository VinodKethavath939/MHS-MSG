#!/usr/bin/env python3
"""
Automated Chrome & ChromeDriver Setup Script
Checks Chrome version and provides download link for matching ChromeDriver
"""

import os
import sys
import subprocess
import platform
import json

def get_chrome_version_windows():
    """Get Chrome version on Windows"""
    try:
        # Try standard installation path
        chrome_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        ]
        
        for path in chrome_paths:
            if os.path.exists(path):
                # Get version using wmic
                try:
                    result = subprocess.check_output(
                        f'wmic datafile where name="{path}" get Version /value',
                        shell=True, 
                        universal_newlines=True
                    )
                    version = result.split('=')[1].strip()
                    return version, path
                except:
                    # Fallback: try getting from file properties
                    import struct
                    
                    def get_file_version(fpath):
                        try:
                            info = os.stat(fpath)
                            # This is a simplified version getter
                            return "unknown"
                        except:
                            return None
                    
                    version = get_file_version(path)
                    if version:
                        return version, path
        
        return None, None
    except Exception as e:
        print(f"Error getting Chrome version: {e}")
        return None, None

def get_chrome_version_from_registry():
    """Get Chrome version from Windows Registry"""
    try:
        import winreg
        
        reg_path = r"Software\Google\Chrome\Binaries"
        try:
            reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path)
            version, _ = winreg.QueryValueEx(reg_key, "pv")
            return version
        except WindowsError:
            pass
        
        # Try machine registry
        reg_path = r"Software\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe"
        try:
            reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path)
            chrome_path, _ = winreg.QueryValueEx(reg_key, "Path")
            
            # Try to get version from executable
            if os.path.exists(chrome_path):
                try:
                    result = subprocess.check_output(
                        [chrome_path, '--version'],
                        stderr=subprocess.DEVNULL,
                        universal_newlines=True
                    )
                    version = result.strip().split()[-1]
                    return version
                except:
                    pass
        except WindowsError:
            pass
        
        return None
    except Exception as e:
        print(f"Error reading registry: {e}")
        return None

def get_chrome_version():
    """Get Chrome version across platforms"""
    system = platform.system()
    
    print("\n" + "="*70)
    print("STEP 1: DETECTING CHROME INSTALLATION")
    print("="*70)
    
    if system == "Windows":
        # Try registry first
        version = get_chrome_version_from_registry()
        
        if not version:
            # Try file system
            version, path = get_chrome_version_windows()
            
            if version and path:
                print(f"✓ Chrome found at: {path}")
                print(f"✓ Chrome version: {version}")
                return version
        else:
            print(f"✓ Chrome version: {version}")
            return version
        
        print("✗ Chrome not found. Please install from: https://google.com/chrome/")
        return None
    
    elif system == "Darwin":  # macOS
        try:
            result = subprocess.check_output(
                ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "--version"],
                universal_newlines=True
            )
            version = result.strip().split()[-1]
            print(f"✓ Chrome version: {version}")
            return version
        except:
            print("✗ Chrome not found on macOS")
            return None
    
    elif system == "Linux":
        try:
            result = subprocess.check_output(
                ["google-chrome", "--version"],
                universal_newlines=True
            )
            version = result.strip().split()[-1]
            print(f"✓ Chrome version: {version}")
            return version
        except:
            print("✗ Chrome not found on Linux")
            return None
    
    return None

def get_major_version(version_string):
    """Extract major version number"""
    if not version_string:
        return None
    
    try:
        # Handle versions like "125.0.6422.142"
        major = version_string.split('.')[0]
        return major
    except:
        return None

def generate_download_link(major_version):
    """Generate ChromeDriver download link"""
    if not major_version:
        return None
    
    return f"https://chromedriver.chromium.org/downloads/version-{major_version}0-branch-branches-heads-{major_version}.0"

def main():
    """Main function"""
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*68 + "║")
    print("║" + "  CHROME & CHROMEDRIVER SETUP WIZARD".center(68) + "║")
    print("║" + " "*68 + "║")
    print("╚" + "="*68 + "╝")
    
    # Step 1: Get Chrome version
    chrome_version = get_chrome_version()
    
    if not chrome_version:
        print("\n⚠️  SETUP CANNOT CONTINUE")
        print("Please install Google Chrome first from: https://google.com/chrome/")
        print("\nAfter installing Chrome, run this script again.")
        return False
    
    # Step 2: Extract major version
    major_version = get_major_version(chrome_version)
    
    print("\n" + "="*70)
    print("STEP 2: CHROMEDRIVER DOWNLOAD")
    print("="*70)
    
    print(f"\n✓ Your Chrome version: {chrome_version}")
    print(f"✓ Major version: {major_version}")
    print(f"\n📥 You need ChromeDriver version: {major_version}")
    
    # Step 3: Provide download instructions
    print("\n" + "="*70)
    print("DOWNLOAD INSTRUCTIONS")
    print("="*70)
    
    download_page = f"https://chromedriver.chromium.org/download"
    
    print(f"\n1. Open this link in your browser:")
    print(f"   {download_page}")
    
    print(f"\n2. Find version {major_version} and click 'Download'")
    
    print(f"\n3. Select your operating system:")
    if platform.system() == "Windows":
        print(f"   → win64 (for most Windows)")
        print(f"   → win32 (for older 32-bit systems)")
    elif platform.system() == "Darwin":
        print(f"   → mac-x64 (Intel)")
        print(f"   → mac-arm64 (Apple Silicon)")
    elif platform.system() == "Linux":
        print(f"   → linux64")
    
    print(f"\n4. Wait for download to complete (~20-30 MB)")
    
    print(f"\n5. Extract the ZIP file")
    
    print(f"\n6. Find: chromedriver.exe (or chromedriver on Mac/Linux)")
    
    # Step 4: Configure .env
    print("\n" + "="*70)
    print("STEP 3: CONFIGURE .ENV FILE")
    print("="*70)
    
    env_file = ".env"
    
    if os.path.exists(env_file):
        print(f"\n✓ Found .env file")
        
        # Read current content
        with open(env_file, 'r') as f:
            content = f.read()
        
        if 'CHROME_DRIVER_PATH' in content:
            print(f"✓ CHROME_DRIVER_PATH already exists in .env")
            print(f"\nUpdate this line with your ChromeDriver path:")
            print(f"CHROME_DRIVER_PATH = /path/to/chromedriver")
            
            print(f"\nExamples:")
            if platform.system() == "Windows":
                print(f"  Windows: CHROME_DRIVER_PATH = C:/Users/vinod/Downloads/chromedriver.exe")
            elif platform.system() == "Darwin":
                print(f"  macOS: CHROME_DRIVER_PATH = /Applications/chromedriver")
            elif platform.system() == "Linux":
                print(f"  Linux: CHROME_DRIVER_PATH = /home/user/chromedriver")
        else:
            print(f"⚠️  CHROME_DRIVER_PATH not found in .env")
            print(f"Add this line to your .env file:")
            print(f"CHROME_DRIVER_PATH = /path/to/chromedriver")
    else:
        print(f"⚠️  .env file not found at: {os.path.abspath(env_file)}")
        print(f"Make sure you're in the correct directory")
    
    # Step 5: Summary
    print("\n" + "="*70)
    print("NEXT STEPS")
    print("="*70)
    
    print(f"\n1. Download ChromeDriver {major_version} from:")
    print(f"   https://chromedriver.chromium.org/download")
    
    print(f"\n2. Extract the ZIP file")
    
    print(f"\n3. Update .env with the path:")
    print(f"   CHROME_DRIVER_PATH = /path/to/chromedriver")
    
    print(f"\n4. Restart Django server:")
    print(f"   Ctrl+C (stop current server)")
    print(f"   python manage.py runserver")
    
    print(f"\n5. Test WhatsApp sending:")
    print(f"   Go to http://localhost:8000")
    print(f"   Create and send a test message")
    
    print(f"\n" + "="*70)
    print(f"✅ SETUP COMPLETE - Follow the steps above!")
    print(f"="*70 + "\n")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
