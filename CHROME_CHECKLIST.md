# ✅ CHROME SETUP CHECKLIST

## Copy and paste this URL into your browser:
```
https://chromedriver.chromium.org/download
```

---

## 🎯 COMPLETE THESE STEPS IN ORDER:

### ✅ STEP 1: Get Your Chrome Version
- [ ] Open Chrome
- [ ] Go to: `chrome://version/`
- [ ] Write down the version number you see
  - Example: "Version 125.0.6422.142"
  - **Just need the first number: 125**

**My Chrome Version: ________________**

---

### ✅ STEP 2: Download Matching ChromeDriver
- [ ] Go to: https://chromedriver.chromium.org/download
- [ ] Find your version (e.g., 125)
- [ ] Click to expand that version
- [ ] Select "win64" (for Windows 64-bit)
- [ ] Click Download
- [ ] Wait for file to download (20-30 MB)

**File downloaded to:** `C:\Users\vinod\Downloads\chromedriver-win64.zip`

---

### ✅ STEP 3: Extract the ZIP File
- [ ] Open File Explorer
- [ ] Go to Downloads folder: `C:\Users\vinod\Downloads\`
- [ ] Find file: `chromedriver-win64.zip`
- [ ] Right-click on it
- [ ] Select: "Extract All..."
- [ ] Click: Extract
- [ ] Wait for extraction

**After extraction, you should have:**
```
C:\Users\vinod\Downloads\chromedriver-win64\
  ├─ chromedriver.exe  ← This is what you need!
  └─ LICENSE.chromium
```

---

### ✅ STEP 4: Update .env File
- [ ] Open file: `C:\Users\vinod\Desktop\MHS MSG\school_whatsapp_system\.env`
- [ ] Find this line:
  ```
  CHROME_DRIVER_PATH = C:/Users/vinod/Downloads/chromedriver.exe
  ```
- [ ] Replace with:
  ```
  CHROME_DRIVER_PATH = C:/Users/vinod/Downloads/chromedriver-win64/chromedriver.exe
  ```
- [ ] Make sure to use **forward slashes** `/` not backslashes `\`
- [ ] Save file (Ctrl+S)

---

### ✅ STEP 5: Test ChromeDriver
- [ ] Open PowerShell (Windows Key + R, type `powershell`)
- [ ] Type this command:
  ```powershell
  cd "C:\Users\vinod\Downloads\chromedriver-win64"
  .\chromedriver.exe --version
  ```
- [ ] You should see: `ChromeDriver 125.0.6422.142`
- [ ] If you see this → SUCCESS! ✅

---

### ✅ STEP 6: Restart Django Server
- [ ] Open PowerShell in the project folder:
  ```powershell
  cd "C:\Users\vinod\Desktop\MHS MSG\school_whatsapp_system"
  ```
- [ ] If server is running, stop it: **Ctrl+C**
- [ ] Start server again:
  ```powershell
  python manage.py runserver
  ```
- [ ] You should see: `Starting development server at http://127.0.0.1:8000/`

---

### ✅ STEP 7: Test WhatsApp Sending
- [ ] Open browser: http://localhost:8000
- [ ] Login with: `admin` / `admin123`
- [ ] Go to: **Messages → Send New Message**
- [ ] Create a test message (any text)
- [ ] Click: **Send**
- [ ] Watch Chrome open automatically
- [ ] See WhatsApp Web with QR code
- [ ] Scan QR code with your phone's WhatsApp
- [ ] Message sends! 🎉

---

## 📋 TROUBLESHOOTING

### ❌ "ChromeDriver not found"
- [ ] Check path in .env is correct
- [ ] Make sure file exists at that location
- [ ] Use forward slashes `/`
- [ ] Restart server

### ❌ "Chrome version mismatch"
- [ ] Get Chrome version: `chrome://version/`
- [ ] Download EXACT matching ChromeDriver version
- [ ] Extract and update .env
- [ ] Restart server

### ❌ "Chrome won't open"
- [ ] Delete session folder:
  ```
  C:\Users\vinod\AppData\Local\WhatsAppSelenium
  ```
- [ ] Try sending again (fresh QR code)

### ❌ "Still not working"
- [ ] Check logs: `whatsapp_app/logs/whatsapp.log`
- [ ] Verify Chrome installed: `chrome://version/`
- [ ] Verify ChromeDriver version matches Chrome version
- [ ] Restart server and try again

---

## 🆘 NEED HELP?

### Run Automated Detector:
```powershell
cd "C:\Users\vinod\Desktop\MHS MSG\school_whatsapp_system"
python chrome_auto_detector.py
```

This will:
- ✓ Detect your Chrome version
- ✓ Tell you what to download
- ✓ Show download link
- ✓ Verify everything is configured

---

## 📞 SUMMARY

**What to download:**
- Chrome version from your computer
- Matching ChromeDriver version
- Extract to Downloads folder
- Update .env with path
- Restart server
- Test sending message

**If Chrome 125:**
- Download ChromeDriver 125 from: https://chromedriver.chromium.org/download

**If Chrome 124:**
- Download ChromeDriver 124 from: https://chromedriver.chromium.org/download

**VERSIONS MUST MATCH EXACTLY!**

---

## ✨ YOU'RE DONE WHEN:

- ✅ Chrome opens automatically when sending messages
- ✅ QR code appears in Chrome
- ✅ You scan QR with WhatsApp phone
- ✅ Messages send successfully
- ✅ Progress bar shows 100%

---

**TOTAL TIME: ~30 minutes**

Start with **STEP 1** now! 🚀

