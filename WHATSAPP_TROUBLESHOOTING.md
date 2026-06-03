# 🔧 WhatsApp Automation Troubleshooting Guide

## ❌ Issue: WhatsApp Web is not opening / Messages not sending

---

## 🚨 QUICK FIX STEPS

### Step 1: Verify Chrome is Installed
1. Open any browser and go to `chrome://version/`
2. **Note the Chrome version** (e.g., "Version 125.0.6422.142")
3. Close the browser

### Step 2: Download ChromeDriver
1. Go to https://chromedriver.chromium.org/
2. Click "Download ChromeDriver"
3. **Select the version matching your Chrome version** (e.g., if you have Chrome 125, download ChromeDriver 125)
4. Extract the ZIP file
5. Save `chromedriver.exe` to a known location (e.g., `C:\Users\vinod\Downloads\`)
6. **Copy the full path** (e.g., `C:\Users\vinod\Downloads\chromedriver.exe`)

### Step 3: Update .env File
1. Open file: `school_whatsapp_system\.env`
2. Find this line:
   ```
   CHROME_DRIVER_PATH = C:/Users/vinod/Downloads/chromedriver.exe
   ```
3. Replace with your actual ChromeDriver path
4. **Use forward slashes** `/` (not backslashes `\`)
5. Save the file

### Step 4: Run Migrations (if not done yet)
```bash
cd c:\Users\vinod\Desktop\MHS MSG\school_whatsapp_system
python manage.py migrate
python manage.py initialize_app
```

### Step 5: Start the Server
```bash
python manage.py runserver
```

### Step 6: Test WhatsApp Connection
1. Open http://localhost:8000
2. Login with: `admin` / `admin123`
3. Go to: Messages → Send New Message
4. Create a test message with any content
5. Click "Send"
6. **A Chrome browser window should open automatically**
7. You'll see the **WhatsApp Web QR Code**
8. **Scan the QR code with your WhatsApp mobile phone** within 60 seconds
9. The message should send!

---

## 🔍 COMMON PROBLEMS & SOLUTIONS

### Problem 1: "ChromeDriver not found"
**Error Message:**
```
selenium.common.exceptions.WebDriverException: Message: [Errno 2] No such file or directory
```

**Solution:**
- Verify ChromeDriver path in `.env` file is correct
- Make sure file exists at that location: `C:\Users\vinod\Downloads\chromedriver.exe`
- Restart the server after updating `.env`

---

### Problem 2: "Chrome version mismatch"
**Error Message:**
```
This version of ChromeDriver only supports Chrome version X
```

**Solution:**
1. Check your Chrome version: `chrome://version/`
2. Download the **matching ChromeDriver version** from https://chromedriver.chromium.org/
3. Replace the old `chromedriver.exe`
4. Restart server and try again

---

### Problem 3: "Connection refused"
**Error Message:**
```
selenium.common.exceptions.WebDriverException: Unable to connect to localhost:9515
```

**Solution:**
- Wait 10 seconds and try again (Chrome takes time to start)
- Check if another Chrome instance is running
- Restart the server
- Make sure port 9515 is not blocked by firewall

---

### Problem 4: "QR Code not appearing"
**Error Message:**
```
QR code element not found / Timeout waiting for QR code
```

**Solution:**
1. Close Chrome completely (all windows)
2. Delete the WhatsApp session directory:
   ```
   C:\Users\vinod\AppData\Local\WhatsAppSelenium
   ```
3. Try sending a message again
4. A fresh QR code should appear
5. Scan it with your WhatsApp phone

---

### Problem 5: "Message not sending after QR scan"
**Possible causes & solutions:**

#### A. WhatsApp not fully loaded
- Wait 10-15 seconds after QR scan completes
- Don't close the browser window
- Check that WhatsApp Web shows the chat list

#### B. Contact phone number format incorrect
- Phone should be 10-12 digits
- Format: `919876543210` (for India: +91 prefix)
- Or: `9876543210` (without prefix, will add +91)

#### C. Contact doesn't exist in WhatsApp
- Make sure the contact exists in your WhatsApp
- Contact must have saved your number in their phone
- Try sending to a known contact first for testing

#### D. Rate limiting (blocked)
- If you send too many messages, WhatsApp blocks you
- Wait 1-2 hours before trying again
- Reduce `WHATSAPP_MESSAGE_DELAY` only slightly (minimum 2 seconds)

---

## 🧪 MANUAL TEST PROCEDURE

### Test 1: Verify ChromeDriver Works
```bash
cd c:\Users\vinod\Desktop\MHS MSG\school_whatsapp_system
python

# In Python shell:
from selenium import webdriver
driver = webdriver.Chrome('C:/Users/vinod/Downloads/chromedriver.exe')
driver.get('https://web.whatsapp.com')
print("Chrome opened successfully!")
driver.quit()
```

If Chrome opens and loads WhatsApp Web, ChromeDriver is working!

### Test 2: Test WhatsApp Connection
```bash
python manage.py shell

# In Django shell:
from whatsapp_app.whatsapp_sender import WhatsAppSender

sender = WhatsAppSender()
print("Testing WhatsApp sender...")

try:
    sender.setup_driver()
    print("✓ Chrome driver initialized")
    
    sender.open_whatsapp_web()
    print("✓ WhatsApp Web opened")
    print("Scan QR code within 60 seconds...")
    
    # Wait for manual QR scan
    input("Press Enter when done scanning QR code: ")
    
    # Try searching a contact
    sender.search_and_open_contact("919876543210")  # Replace with actual number
    print("✓ Contact found and opened")
    
    sender.close()
    print("✓ Connection test successful!")
    
except Exception as e:
    print(f"✗ Error: {e}")
    sender.close()
```

---

## 📋 DEBUGGING CHECKLIST

- [ ] Chrome installed and version checked
- [ ] ChromeDriver downloaded (matching Chrome version)
- [ ] ChromeDriver path updated in `.env` file
- [ ] `.env` file uses forward slashes `/`
- [ ] Server restarted after .env changes
- [ ] WhatsApp Web session directory cleared (if switching phones)
- [ ] Tested with admin account first
- [ ] Proper phone number format (10-12 digits)
- [ ] Contact exists in WhatsApp
- [ ] Waited 10+ seconds after QR scan
- [ ] Not rate limited by WhatsApp
- [ ] Chrome window not closed during sending

---

## 📱 PHONE NUMBER FORMATS

### For India (most common):
```
✓ 919876543210    (with +91)
✓ 9876543210      (without +91, will add automatically)
✗ 91 9876543210   (spaces)
✗ +91-9876543210  (hyphens)
```

### For Other Countries:
- **USA**: `14155552671` (1 + area code + number)
- **UK**: `442071838750` (44 + number without leading 0)
- **Format**: Country code + number (no +, spaces, or hyphens)

---

## 🛠️ ADVANCED TROUBLESHOOTING

### Enable Debug Logging
Edit `school_notification/settings.py`:
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',  # Change to DEBUG
            'class': 'logging.FileHandler',
            'filename': 'whatsapp_app/logs/whatsapp.log',
        },
    },
    'loggers': {
        'whatsapp_app': {
            'handlers': ['file'],
            'level': 'DEBUG',  # Change to DEBUG
            'propagate': True,
        },
    },
}
```

Then check logs:
```bash
tail -f whatsapp_app/logs/whatsapp.log
```

### Check Chrome Process
```powershell
Get-Process chrome
```

If Chrome is stuck, kill it:
```powershell
Stop-Process -Name chrome -Force
```

---

## ✅ SUCCESS INDICATORS

When WhatsApp automation works correctly, you should see:

1. **Dashboard** shows "Connected" status
2. **Chrome browser** opens automatically when sending
3. **QR code** appears in Chrome browser
4. **After scanning**: Chat list appears with search box
5. **Message sending**: Visible in Chrome window
6. **Message logs**: Show "SENT" status
7. **Progress bar**: Shows 100% when complete

---

## 📞 FINAL VERIFICATION

After following all steps above:

1. **Verify .env:**
   ```bash
   type .env | findstr "CHROME_DRIVER_PATH"
   ```
   Should show your ChromeDriver path

2. **Verify Chrome/ChromeDriver:**
   ```bash
   cd C:\Users\vinod\Downloads
   chromedriver --version
   ```
   Should show: "ChromeDriver 125.0.6..." (or your version)

3. **Test message sending:**
   - Login at http://localhost:8000
   - Upload a test contact
   - Send a message
   - Watch Chrome open and complete the send

---

## 🚀 QUICK RESTART GUIDE

If nothing works, restart completely:

```bash
# 1. Stop server (Ctrl+C in terminal)

# 2. Clear Chrome session
Remove-Item -Path "$env:APPDATA\Local\WhatsAppSelenium" -Recurse -Force

# 3. Restart server
python manage.py runserver

# 4. Try sending again
```

---

## 📚 RESOURCES

- ChromeDriver Downloads: https://chromedriver.chromium.org/
- WhatsApp Web: https://web.whatsapp.com
- Chrome Version Check: chrome://version/
- Selenium Documentation: https://www.selenium.dev/documentation/

---

**If you've completed all steps above and still have issues, check:**

1. Windows Firewall blocking Chrome
2. Antivirus blocking ChromeDriver
3. Chrome browser cache (clear browsing data)
4. Network connectivity to web.whatsapp.com
5. WhatsApp account issues (try web.whatsapp.com manually first)

---

**Status**: After following this guide, WhatsApp should work! 🎉

