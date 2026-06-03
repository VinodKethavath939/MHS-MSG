#!/usr/bin/env python
"""
Quick start script for School WhatsApp Notification System
This script automates the initial setup process
"""

import os
import sys
import subprocess
from pathlib import Path


def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")


def print_step(text):
    """Print step message"""
    print(f"▶ {text}")


def print_success(text):
    """Print success message"""
    print(f"✓ {text}")


def print_error(text):
    """Print error message"""
    print(f"✗ {text}")


def check_python():
    """Check Python version"""
    print_step("Checking Python version...")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print_error(f"Python 3.9+ required. Found: {version.major}.{version.minor}")
        return False
    
    print_success(f"Python {version.major}.{version.minor}.{version.micro}")
    return True


def check_chrome():
    """Check if Chrome is installed"""
    print_step("Checking Google Chrome installation...")
    
    # Common Chrome paths
    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expandvars(r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"),
        os.path.expandvars(r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"),
    ]
    
    for chrome_path in chrome_paths:
        if os.path.exists(chrome_path):
            print_success(f"Chrome found at: {chrome_path}")
            return True
    
    print_error("Google Chrome not found. Please install Chrome from https://www.google.com/chrome/")
    return False


def create_venv():
    """Create virtual environment"""
    print_step("Creating virtual environment...")
    
    venv_path = Path("venv")
    if venv_path.exists():
        print_success("Virtual environment already exists")
        return True
    
    try:
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print_success("Virtual environment created")
        return True
    except subprocess.CalledProcessError:
        print_error("Failed to create virtual environment")
        return False


def get_venv_python():
    """Get path to Python in virtual environment"""
    if sys.platform == "win32":
        return Path("venv/Scripts/python.exe")
    else:
        return Path("venv/bin/python")


def install_dependencies():
    """Install Python dependencies"""
    print_step("Installing Python dependencies...")
    
    python_path = get_venv_python()
    
    try:
        subprocess.run(
            [str(python_path), "-m", "pip", "install", "--upgrade", "pip"],
            check=True
        )
        subprocess.run(
            [str(python_path), "-m", "pip", "install", "-r", "requirements.txt"],
            check=True
        )
        print_success("Dependencies installed")
        return True
    except subprocess.CalledProcessError:
        print_error("Failed to install dependencies")
        return False


def create_env_file():
    """Create .env file from example"""
    print_step("Creating .env file...")
    
    env_path = Path(".env")
    env_example = Path(".env.example")
    
    if env_path.exists():
        print_success(".env file already exists")
        return True
    
    if env_example.exists():
        try:
            with open(env_example, 'r') as f:
                content = f.read()
            with open(env_path, 'w') as f:
                f.write(content)
            print_success(".env file created (from .env.example)")
            return True
        except Exception as e:
            print_error(f"Failed to create .env file: {str(e)}")
            return False
    else:
        # Create basic .env
        env_content = """SECRET_KEY = django-insecure-school-whatsapp-notification-system-dev
DEBUG = True
CHROME_DRIVER_PATH = chromedriver.exe
WHATSAPP_MESSAGE_DELAY = 2
"""
        try:
            with open(env_path, 'w') as f:
                f.write(env_content)
            print_success(".env file created")
            return True
        except Exception as e:
            print_error(f"Failed to create .env file: {str(e)}")
            return False


def run_migrations():
    """Run Django migrations"""
    print_step("Setting up database...")
    
    python_path = get_venv_python()
    
    try:
        subprocess.run(
            [str(python_path), "manage.py", "migrate"],
            check=True
        )
        print_success("Database setup completed")
        return True
    except subprocess.CalledProcessError:
        print_error("Failed to run migrations")
        return False


def initialize_app():
    """Initialize application"""
    print_step("Initializing application...")
    
    python_path = get_venv_python()
    
    try:
        subprocess.run(
            [str(python_path), "manage.py", "initialize_app"],
            check=True
        )
        print_success("Application initialized")
        return True
    except subprocess.CalledProcessError:
        print_error("Failed to initialize application")
        return False


def main():
    """Main setup process"""
    print_header("School WhatsApp Notification System - Setup")
    
    steps = [
        ("Checking Python", check_python),
        ("Checking Chrome", check_chrome),
        ("Creating Virtual Environment", create_venv),
        ("Installing Dependencies", install_dependencies),
        ("Creating Environment File", create_env_file),
        ("Setting Up Database", run_migrations),
        ("Initializing Application", initialize_app),
    ]
    
    completed = 0
    
    for step_name, step_func in steps:
        print_header(step_name)
        if step_func():
            completed += 1
        else:
            print_error(f"Setup stopped at: {step_name}")
            break
    
    # Final status
    print_header(f"Setup Status: {completed}/{len(steps)} steps completed")
    
    if completed == len(steps):
        print_success("Setup completed successfully!")
        print("\nNext steps:")
        print("1. Download ChromeDriver from: https://chromedriver.chromium.org/downloads")
        print("2. Update CHROME_DRIVER_PATH in .env file")
        print("3. Run: python manage.py runserver")
        print("4. Open: http://localhost:8000")
        print("5. Login with: admin / admin123")
        print("\n⚠️  Change admin password immediately!")
    else:
        print_error("Setup not completed. Please fix the errors above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
