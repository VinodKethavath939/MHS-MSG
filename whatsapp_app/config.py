"""
Configuration and setup utilities for the WhatsApp notification system
"""

import os
import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class Config:
    """Central configuration management"""
    
    # Base directory
    BASE_DIR = Path(__file__).resolve().parent.parent
    
    # ChromeDriver Settings
    CHROMEDRIVER_PATH = os.getenv('CHROME_DRIVER_PATH', 'chromedriver.exe')
    
    # WhatsApp Settings
    WHATSAPP_MESSAGE_DELAY = int(os.getenv('WHATSAPP_MESSAGE_DELAY', 2))
    WHATSAPP_TIMEOUT = int(os.getenv('WHATSAPP_TIMEOUT', 60))
    WHATSAPP_SESSION_TIMEOUT = int(os.getenv('WHATSAPP_SESSION_TIMEOUT', 300))
    
    # Session Directory
    USER_DATA_DIR = str(Path.home() / 'AppData' / 'Local' / 'WhatsAppSelenium')
    
    @staticmethod
    def get_all_config():
        """Get all configuration as dictionary"""
        return {
            'chromedriver_path': Config.CHROMEDRIVER_PATH,
            'message_delay': Config.WHATSAPP_MESSAGE_DELAY,
            'timeout': Config.WHATSAPP_TIMEOUT,
            'session_timeout': Config.WHATSAPP_SESSION_TIMEOUT,
            'user_data_dir': Config.USER_DATA_DIR,
        }


def setup_directories():
    """Create necessary directories"""
    dirs = [
        Config.BASE_DIR / 'whatsapp_app' / 'static' / 'uploads',
        Config.BASE_DIR / 'whatsapp_app' / 'logs',
        Config.USER_DATA_DIR,
    ]
    
    for directory in dirs:
        directory.mkdir(parents=True, exist_ok=True)
        logger.info(f"Directory ready: {directory}")


def create_superuser():
    """Create default superuser"""
    from django.contrib.auth.models import User
    
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@school.local', 'admin123')
        logger.info("Default admin user created: admin / admin123")
    else:
        logger.info("Admin user already exists")


def create_sample_school():
    """Create sample school setting"""
    from django.contrib.auth.models import User
    from whatsapp_app.models import SchoolSetting
    
    try:
        admin = User.objects.get(username='admin')
        if not SchoolSetting.objects.filter(admin_user=admin).exists():
            SchoolSetting.objects.create(
                school_name='Demo School',
                admin_user=admin
            )
            logger.info("Sample school created")
    except User.DoesNotExist:
        logger.warning("Admin user not found. Create admin first.")


def initialize_app():
    """Initialize application on startup"""
    setup_directories()
    
    try:
        import django
        django.setup()
        
        create_superuser()
        create_sample_school()
        logger.info("Application initialization completed")
    except Exception as e:
        logger.error(f"Error during initialization: {str(e)}")
