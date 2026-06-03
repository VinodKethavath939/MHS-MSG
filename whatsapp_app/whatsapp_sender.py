"""
WhatsApp Sender - Hybrid Mode
Automatically uses real Selenium if ChromeDriver is available
Falls back to demo mode if Chrome/ChromeDriver not found
"""

import os
import time
import logging
import random
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

# Try to import Selenium - if not available or Chrome missing, use demo mode
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.service import Service
    from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
    logger.info("Selenium not available - using demo mode")


class WhatsAppSender:
    """
    WhatsApp Sender - Hybrid Mode
    
    Automatically detects and uses:
    1. Real Selenium with Chrome (if ChromeDriver found)
    2. Demo simulation mode (fallback)
    """

    def __init__(self, chrome_driver_path='chromedriver.exe', demo_mode=None):
        """Initialize WhatsApp sender"""
        self.chrome_driver_path = chrome_driver_path
        self.driver = None
        self.wait = None
        self.is_ready = False
        self.message_count = 0
        self.successful_sends = 0
        self.failed_sends = 0
        self.user_data_dir = str(Path.home() / 'AppData' / 'Local' / 'WhatsAppSelenium')
        
        # Auto-detect mode
        if demo_mode is None:
            self.demo_mode = not self._check_chromedriver_available()
        else:
            self.demo_mode = demo_mode
        
        if self.demo_mode:
            logger.info("🎭 Running in DEMO MODE (ChromeDriver not found)")
        else:
            logger.info("✓ Running in PRODUCTION MODE (ChromeDriver detected)")
        
    def _check_chromedriver_available(self):
        """Check if ChromeDriver is available"""
        if not SELENIUM_AVAILABLE:
            return False
        
        # Check various common locations
        possible_paths = [
            Path(self.chrome_driver_path),
            Path('chromedriver.exe'),
            Path.cwd() / 'chromedriver.exe',
            Path.home() / 'Downloads' / 'chromedriver-win64' / 'chromedriver.exe',
            Path.home() / 'Downloads' / 'chromedriver-win64' / 'chromedriver-win64' / 'chromedriver.exe',
            Path('C:/Users/vinod/Downloads/chromedriver-win64/chromedriver.exe'),
            Path('C:/Users/vinod/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe'),
        ]
        
        for path in possible_paths:
            if path.exists():
                logger.info(f"Found ChromeDriver at: {path}")
                self.chrome_driver_path = str(path)
                return True
        
        return False

    def setup_driver(self):
        """Setup driver (auto-detects real vs demo mode)"""
        if self.demo_mode:
            return self._setup_demo()
        else:
            return self._setup_real()
    
    def _setup_real(self):
        """Setup real Chrome WebDriver"""
        try:
            logger.info("Setting up Chrome WebDriver...")
            
            options = webdriver.ChromeOptions()
            options.add_argument(f'--user-data-dir={self.user_data_dir}')
            options.add_argument('--profile-directory=Default')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--start-maximized')
            options.add_argument('--disable-notifications')
            
            try:
                service = Service(self.chrome_driver_path)
                self.driver = webdriver.Chrome(service=service, options=options)
            except TypeError:
                # Fallback for older Selenium versions that do not accept 'service'
                self.driver = webdriver.Chrome(executable_path=self.chrome_driver_path, options=options)
            self.wait = WebDriverWait(self.driver, 30)
            
            logger.info("✓ WebDriver setup successful")
            self.is_ready = True
            return True
            
        except Exception as e:
            logger.error(f"Failed to setup WebDriver: {str(e)}")
            logger.info("Falling back to demo mode...")
            self.demo_mode = True
            return self._setup_demo()
    
    def _setup_demo(self):
        """Setup demo mode"""
        try:
            logger.info("🎭 Initializing WhatsApp sender (demo mode)...")
            time.sleep(0.5)
            logger.info("✓ WhatsApp sender ready (demo mode)")
            self.is_ready = True
            return True
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            return False

    def open_whatsapp_web(self):
        """Open WhatsApp Web"""
        if self.demo_mode:
            return self._open_whatsapp_web_demo()
        else:
            return self._open_whatsapp_web_real()
    
    def _open_whatsapp_web_real(self):
        """Real WhatsApp Web opening with Selenium"""
        try:
            logger.info("Opening WhatsApp Web...")
            self.driver.get('https://web.whatsapp.com')
            
            try:
                self.wait.until(EC.presence_of_element_located(
                    (By.XPATH, "//div[@data-testid='chat-list'] | //div[@id='pane-side'] | //div[@contenteditable='true'][@data-tab='3'] | //div[@role='textbox']")
                ))
                logger.info("✓ Already logged in to WhatsApp")
                self.is_ready = True
                return True
            except TimeoutException:
                try:
                    self.wait.until(EC.presence_of_element_located(
                        (By.XPATH, "//canvas[@data-testid='qrcode'] | //canvas[@aria-label='Scan me!'] | //div[@data-testid='qrcode'] | //div[@aria-label='Scan me!']")
                    ))
                    logger.info("QR code displayed. Please scan with your phone.")
                    time.sleep(2)
                    self.wait.until(EC.invisibility_of_element_located(
                        (By.XPATH, "//canvas[@data-testid='qrcode'] | //canvas[@aria-label='Scan me!'] | //div[@data-testid='qrcode'] | //div[@aria-label='Scan me!']")
                    ), timeout=300)
                    self.wait.until(EC.presence_of_element_located(
                        (By.XPATH, "//div[@data-testid='chat-list'] | //div[@id='pane-side'] | //div[@contenteditable='true'][@data-tab='3'] | //div[@role='textbox']")
                    ))
                    logger.info("✓ QR code scanned successfully")
                    self.is_ready = True
                    return True
                except TimeoutException:
                    logger.error("QR code scan timeout (waited 5 minutes)")
                    return False
                    
        except Exception as e:
            logger.error(f"Error opening WhatsApp Web: {str(e)}")
            return False
    
    def _open_whatsapp_web_demo(self):
        """Demo mode WhatsApp Web opening"""
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
        """Search and open contact"""
        if self.demo_mode:
            return self._search_and_open_contact_demo(phone_number)
        else:
            return self._search_and_open_contact_real(phone_number)
    
    def _search_and_open_contact_real(self, phone_number):
        """Real contact search with Selenium"""
        try:
            logger.info(f"Opening chat for: {phone_number}")
            digits_only = ''.join(ch for ch in str(phone_number) if ch.isdigit())
            if len(digits_only) == 10:
                digits_only = f"91{digits_only}"
            self.driver.get(f"https://web.whatsapp.com/send?phone={digits_only}&text=&app_absent=0")

            try:
                self.wait.until(EC.presence_of_element_located(
                    (By.XPATH, "//footer//div[@contenteditable='true'][@data-tab='10' or @data-tab='6'] | //footer//div[@role='textbox']")
                ))
                logger.info(f"✓ Chat opened for {digits_only}")
                return True
            except TimeoutException:
                logger.warning(f"Chat not ready for {digits_only}")
                return False
                
        except Exception as e:
            logger.error(f"Error searching contact: {str(e)}")
            return False
    
    def _search_and_open_contact_demo(self, phone_number):
        """Demo contact search"""
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
        """Send message"""
        if self.demo_mode:
            return self._send_message_demo(message, retry_count)
        else:
            return self._send_message_real(message, retry_count)
    
    def _send_message_real(self, message, retry_count=3):
        """Real message sending with Selenium"""
        attempt = 0
        
        while attempt < retry_count:
            try:
                logger.info(f"Sending message (attempt {attempt + 1}/{retry_count})")
                
                message_box = self.wait.until(EC.presence_of_element_located(
                    (By.XPATH, "//footer//div[@contenteditable='true'][@data-tab='10' or @data-tab='6'] | //footer//div[@role='textbox']")
                ))
                
                message_box.click()
                message_box.send_keys(message)
                time.sleep(1)
                
                try:
                    send_button = self.wait.until(EC.element_to_be_clickable(
                        (By.XPATH, "//button[@aria-label='Send'] | //span[@data-icon='send']")
                    ))
                    send_button.click()
                except TimeoutException:
                    # Fallback: press Enter to send
                    message_box.send_keys(Keys.ENTER)
                
                logger.info("✓ Message sent successfully")
                time.sleep(1)
                self.successful_sends += 1
                self.message_count += 1
                return True
                
            except (TimeoutException, NoSuchElementException) as e:
                attempt += 1
                logger.warning(f"Attempt {attempt} failed: {str(e)}")
                if attempt < retry_count:
                    time.sleep(2)
                continue
            except Exception as e:
                logger.error(f"Error sending message: {str(e)}")
                self.failed_sends += 1
                return False
        
        self.failed_sends += 1
        return False
    
    def _send_message_demo(self, message, retry_count=3):
        """Demo message sending"""
        try:
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
        """Close current chat"""
        if not self.demo_mode and self.driver:
            try:
                search_box = self.driver.find_element(
                    By.XPATH, "//div[@contenteditable='true'][@data-tab='3']"
                )
                search_box.clear()
                time.sleep(0.5)
            except Exception as e:
                logger.warning(f"Could not close chat: {str(e)}")
        else:
            try:
                logger.info("🎭 DEMO: Closing chat...")
                time.sleep(0.2)
            except Exception as e:
                logger.warning(f"Could not close chat: {str(e)}")

    def send_bulk_message(self, contacts, message, delay=2, progress_callback=None):
        """Send bulk messages"""
        if not self.is_ready:
            logger.error("WhatsApp not ready")
            return {'sent': [], 'failed': list(contacts)}
        
        results = {'sent': [], 'failed': []}
        
        for index, contact in enumerate(contacts):
            try:
                phone = contact.get('phone')
                name = contact.get('name')
                
                logger.info(f"[{index + 1}/{len(contacts)}] Processing {name}...")
                
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
            if not self.demo_mode and self.driver:
                logger.info("Closing Chrome WebDriver...")
                self.driver.quit()
            else:
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
