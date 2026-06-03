"""
WhatsApp Sender - Demo Mode
Simulates WhatsApp operations without requiring Chrome/ChromeDriver
Use this for testing; replace with Selenium version when Chrome is available
"""

import os
import time
import logging
import random
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


class WhatsAppSender:
    """
    WhatsApp Sender - DEMO MODE
    
    Simulates WhatsApp operations for testing without hardware.
    To use production Selenium version:
    1. Install Chrome browser
    2. Download matching ChromeDriver
    3. Update CHROME_DRIVER_PATH in .env
    4. Replace this file with production version
    """

    def __init__(self, chrome_driver_path='chromedriver.exe', demo_mode=True):
        """Initialize WhatsApp sender"""
        self.chrome_driver_path = chrome_driver_path
        self.driver = None
        self.wait = None
        self.is_ready = False
        self.demo_mode = demo_mode
        self.message_count = 0
        self.successful_sends = 0
        self.failed_sends = 0
        
    def setup_driver(self):
        """Setup driver (demo mode - simulated)"""
        try:
            logger.info("🎭 DEMO: Initializing WhatsApp sender...")
            time.sleep(0.5)
            logger.info("✓ WhatsApp sender ready (demo mode)")
            self.is_ready = True
            return True
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            return False

    def open_whatsapp_web(self):
        """Open WhatsApp Web (demo mode - simulated)"""
        try:
            logger.info("🎭 DEMO: Opening WhatsApp Web...")
            time.sleep(1)
            logger.info("✓ WhatsApp Web loaded (demo mode)")
            self.is_ready = True
            return True
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            return False

    def search_and_open_contact(self, phone_number):
        """Search and open contact (demo mode - simulated)"""
        try:
            phone = str(phone_number).replace('+', '').replace(' ', '').replace('-', '')
            logger.info(f"🎭 DEMO: Searching for contact {phone}...")
            time.sleep(0.3)
            logger.info(f"✓ Contact {phone} found (demo mode)")
            return True
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            return False

    def send_message(self, message, retry_count=3):
        """Send message (demo mode - simulated with 95% success rate)"""
        try:
            # 5% failure rate for realism
            if random.random() > 0.95:
                logger.warning("🎭 DEMO: Send failed (simulated failure)")
                self.failed_sends += 1
                return False
            
            logger.info("🎭 DEMO: Sending message...")
            time.sleep(0.2)
            
            self.message_count += 1
            self.successful_sends += 1
            logger.info(f"✓ Message sent (demo mode) - Total: {self.message_count}")
            return True
            
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            self.failed_sends += 1
            return False

    def close_current_chat(self):
        """Close current chat (demo mode)"""
        try:
            logger.info("🎭 DEMO: Closing chat...")
            time.sleep(0.2)
        except Exception as e:
            logger.warning(f"Could not close chat: {str(e)}")

    def send_bulk_message(self, contacts, message, delay=2, progress_callback=None):
        """Send bulk messages (demo mode - simulated)"""
        if not self.is_ready:
            logger.error("WhatsApp not ready")
            return {'sent': [], 'failed': list(contacts)}
        
        results = {'sent': [], 'failed': []}
        
        for index, contact in enumerate(contacts):
            try:
                phone = contact.get('phone')
                name = contact.get('name')
                
                logger.info(f"🎭 DEMO: [{index + 1}/{len(contacts)}] Processing {name}...")
                
                if not self.search_and_open_contact(phone):
                    results['failed'].append(contact)
                    if progress_callback:
                        progress_callback(index + 1, len(contacts), 'failed')
                    continue
                
                if not self.send_message(message):
                    results['failed'].append(contact)
                    if progress_callback:
                        progress_callback(index + 1, len(contacts), 'failed')
                    continue
                
                results['sent'].append(contact)
                logger.info(f"✓ Message sent to {name}")
                
                if progress_callback:
                    progress_callback(index + 1, len(contacts), 'sent')
                
                time.sleep(delay)
                
            except Exception as e:
                logger.error(f"Error processing {name}: {str(e)}")
                results['failed'].append(contact)
                if progress_callback:
                    progress_callback(index + 1, len(contacts), 'error')
        
        logger.info(f"✓ Bulk send complete: {len(results['sent'])} sent, {len(results['failed'])} failed")
        return results

    def close(self):
        """Close WhatsApp sender"""
        try:
            logger.info("🎭 DEMO: Closing WhatsApp sender...")
            logger.info(f"Stats - Sent: {self.successful_sends}, Failed: {self.failed_sends}")
        except Exception as e:
            logger.error(f"Error closing: {str(e)}")

    def __enter__(self):
        """Context manager entry"""
        self.setup_driver()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()
