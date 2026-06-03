#!/usr/bin/env python
"""
WhatsApp Setup Helper Script
Guides you through setting up ChromeDriver and verifying the installation
"""

import os
import sys
import subprocess
import platform

def check_chrome_installed():
    """Check if Chrome is installed"""
    system = platform.system()
    
    print("\n" + "="*60)
    print("STEP 1: Checking Chrome Installation")
    print("="*60)
    
    if system == 'Windows':
        chrome_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            os.path.expandvars(r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"),
            os.path.expandvars(r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"),
        ]
        
        for path in chrome_paths:
            if os.path.exists(path):
                print(f"✓ Chrome found at: {path}")
                return path
        
        print("✗ Chrome not found. Please install from: https://google.com/chrome/")
        return None
    
    elif system == 'Darwin':  # macOS
        chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        if os.path.exists(chrome_path):
            print(f"✓ Chrome found at: {chrome_path}")
            return chrome_path
        print("✗ Chrome not found. Please install from: https://google.com/chrome/")
        return None
    
    elif system == 'Linux':
        result = os.system('which google-chrome > /dev/null 2>&1')
        if result == 0:
            print("✓ Chrome found in system PATH")
            return "google-chrome"
        print("✗ Chrome not found. Please install: sudo apt-get install google-chrome-stable")
        return None

def get_chrome_version(chrome_path):
    """Get Chrome version"""
    print("\n" + "="*60)
    print("STEP 2: Getting Chrome Version")
    print("="*60)
    
    try:
        if platform.system() == 'Windows':
            import re
            output = subprocess.check_output([chrome_path, '--version']).decode()
            version = re.search(r'(\d+)', output)
            if version:
                print(f"✓ Chrome version: {output.strip()}")
                return version.group(1)
        else:
            output = subprocess.check_output([chrome_path, '--version']).decode()
            print(f"✓ Chrome version: {output.strip()}")
            version_num = output.split()[-1].split('.')[0]
            return version_num
    except Exception as e:
        print(f"✗ Error getting Chrome version: {e}")
        return None

def check_chromedriver():
    """Check if ChromeDriver exists and is configured"""
    print("\n" + "="*60)
    print("STEP 3: Checking ChromeDriver Configuration")
    print("="*60)
    
    # Check for .env file
    env_file = ".env"
    if not os.path.exists(env_file):
        print(f"✗ .env file not found")
        return None
    
    # Read .env file
    with open(env_file, 'r') as f:
        content = f.read()
        if 'CHROME_DRIVER_PATH' in content:
            for line in content.split('\n'):
                if line.startswith('CHROME_DRIVER_PATH'):
                    chromedriver_path = line.split('=')[1].strip().strip('"').strip("'")
                    print(f"✓ Found in .env: CHROME_DRIVER_PATH = {chromedriver_path}")
                    
                    # Expand path if using Windows variables
                    chromedriver_path = os.path.expandvars(chromedriver_path)
                    chromedriver_path = chromedriver_path.replace('\\', os.sep)
                    
                    if os.path.exists(chromedriver_path):
                        print(f"✓ ChromeDriver exists at: {chromedriver_path}")
                        return chromedriver_path
                    else:
                        print(f"✗ ChromeDriver NOT found at: {chromedriver_path}")
                        return None
        else:
            print("✗ CHROME_DRIVER_PATH not found in .env")
            return None

def test_chromedriver(chromedriver_path):
    """Test if ChromeDriver works"""
    print("\n" + "="*60)
    print("STEP 4: Testing ChromeDriver")
    print("="*60)
    
    try:
        output = subprocess.check_output([chromedriver_path, '--version']).decode()
        print(f"✓ ChromeDriver is working: {output.strip()}")
        return True
    except FileNotFoundError:
        print(f"✗ ChromeDriver not found at: {chromedriver_path}")
        return False
    except Exception as e:
        print(f"✗ Error testing ChromeDriver: {e}")
        return False

def run_whatsapp_test():
    """Test WhatsApp connection"""
    print("\n" + "="*60)
    print("STEP 5: Testing WhatsApp Connection")
    print("="*60)
    
    try:
        print("Testing WhatsApp Sender...")
        result = subprocess.run(
            [sys.executable, 'manage.py', 'shell'],
            input="""
from whatsapp_app.whatsapp_sender import WhatsAppSender
from django.conf import settings

chrome_driver = settings.CHROME_DRIVER_PATH
print(f"ChromeDriver path from settings: {chrome_driver}")

sender = WhatsAppSender(chrome_driver_path=chrome_driver)
print("✓ WhatsAppSender initialized successfully!")
""",
            capture_output=True,
            text=True,
            timeout=10
        )
        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"✗ Error testing WhatsApp: {e}")
        return False

def main():
    """Main setup flow"""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*58 + "║")
    print("║" + "  WhatsApp Notification System - Setup Helper".center(58) + "║")
    print("║" + " "*58 + "║")
    print("╚" + "="*58 + "╝")
    
    # Step 1: Check Chrome
    chrome_path = check_chrome_installed()
    if not chrome_path:
        print("\n⚠️ Please install Chrome first from: https://google.com/chrome/")
        return False
    
    # Step 2: Get Chrome version
    chrome_version = get_chrome_version(chrome_path)
    if not chrome_version:
        return False
    
    print(f"\n⚠️ Next, download ChromeDriver version {chrome_version} from:")
    print("   https://chromedriver.chromium.org/download")
    print(f"\n   Or use this direct link:")
    print(f"   https://googlechromelabs.github.io/chrome-for-testing/")
    print("\n   1. Click on version matching your Chrome version")
    print("   2. Download the WIN32/LINUX/MAC version")
    print("   3. Extract chromedriver.exe")
    print("   4. Save to: C:\\Users\\vinod\\Downloads\\chromedriver.exe")
    print("\n   OR provide your own path in the .env file:")
    print("   CHROME_DRIVER_PATH = /path/to/chromedriver.exe")
    
    input("\n⏳ Press Enter once you've downloaded and placed ChromeDriver...")
    
    # Step 3: Check ChromeDriver
    chromedriver_path = check_chromedriver()
    if not chromedriver_path:
        print("\n❌ ChromeDriver not configured properly. Please:")
        print("   1. Download ChromeDriver from https://chromedriver.chromium.org/")
        print("   2. Update CHROME_DRIVER_PATH in .env file")
        return False
    
    # Step 4: Test ChromeDriver
    if not test_chromedriver(chromedriver_path):
        return False
    
    # Step 5: Run migrations
    print("\n" + "="*60)
    print("STEP 5: Running Database Migrations")
    print("="*60)
    
    result = subprocess.run([sys.executable, 'manage.py', 'migrate'], capture_output=True, text=True)
    if result.returncode == 0:
        print("✓ Migrations completed successfully")
    else:
        print(f"✗ Migration error: {result.stderr}")
        return False
    
    # Step 6: Initialize app
    print("\n" + "="*60)
    print("STEP 6: Initializing Application")
    print("="*60)
    
    result = subprocess.run([sys.executable, 'manage.py', 'initialize_app'], capture_output=True, text=True)
    if result.returncode == 0:
        print("✓ Application initialized successfully")
        print(result.stdout)
    else:
        print(f"⚠️ Initialization message: {result.stdout}")
    
    # Final summary
    print("\n" + "="*60)
    print("✅ SETUP COMPLETE!")
    print("="*60)
    print("\nYou're ready to run the application:")
    print("   python manage.py runserver")
    print("\nThen visit:")
    print("   http://localhost:8000")
    print("\nLogin with:")
    print("   Username: admin")
    print("   Password: admin123")
    print("\n⚠️ IMPORTANT: Change your password immediately after login!")
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
