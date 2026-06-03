"""
Comprehensive setup and installation guide for School WhatsApp Notification System
"""

# ============================================================================
# SCHOOL WHATSAPP NOTIFICATION SYSTEM - COMPLETE SETUP GUIDE
# ============================================================================

## TABLE OF CONTENTS
# 1. Prerequisites
# 2. Project Setup
# 3. Database Configuration
# 4. ChromeDriver Setup
# 5. Installation Steps
# 6. Running the Application
# 7. First Time Use
# 8. Troubleshooting
# 9. Using the System

## ============================================================================
## 1. PREREQUISITES
## ============================================================================

Before starting, ensure you have installed:

- **Python 3.9+** (Download from python.org)
- **pip** (comes with Python)
- **Git** (optional, for version control)
- **Google Chrome** (required for WhatsApp automation)
- **PostgreSQL or MySQL** (optional, for production)

Verify installations:
```
python --version
pip --version
```

## ============================================================================
## 2. PROJECT SETUP
## ============================================================================

### 2.1 Extract the Project

Extract the `school_whatsapp_system` folder to your desired location.

### 2.2 Create Virtual Environment

Open Command Prompt and navigate to the project folder:

```bash
cd school_whatsapp_system
python -m venv venv
```

### 2.3 Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 2.4 Install Dependencies

```bash
pip install -r requirements.txt
```

## ============================================================================
## 3. ENVIRONMENT CONFIGURATION
## ============================================================================

### 3.1 Create .env File

Copy `.env.example` to `.env`:

**Windows (PowerShell):**
```powershell
Copy-Item .env.example .env
```

**Windows (Command Prompt):**
```cmd
copy .env.example .env
```

**Linux/Mac:**
```bash
cp .env.example .env
```

### 3.2 Edit .env File

Open `.env` file and update:
- `SECRET_KEY`: Generate a strong secret key
- `CHROME_DRIVER_PATH`: Path to chromedriver
- Database settings (if using PostgreSQL)
- Email settings (optional)

## ============================================================================
## 4. CHROMEDRIVER SETUP
## ============================================================================

### 4.1 Download ChromeDriver

1. Go to: https://chromedriver.chromium.org/downloads
2. Download version matching your Chrome version
3. Extract the zip file
4. Note the path to `chromedriver.exe`

### 4.2 Configure Path in .env

Add ChromeDriver path to `.env`:

```
CHROME_DRIVER_PATH = C:\path\to\chromedriver.exe
```

Or place `chromedriver.exe` in project root folder.

## ============================================================================
## 5. DATABASE SETUP
## ============================================================================

### 5.1 SQLite (Default - Recommended for Testing)

SQLite is configured by default. No additional setup needed.

### 5.2 PostgreSQL (Recommended for Production)

Install PostgreSQL and create database:

```sql
CREATE DATABASE school_whatsapp;
CREATE USER school_admin WITH PASSWORD 'your_password';
ALTER ROLE school_admin SET client_encoding TO 'utf8';
ALTER ROLE school_admin SET default_transaction_isolation TO 'read committed';
ALTER ROLE school_admin SET default_transaction_deferrable TO on;
GRANT ALL PRIVILEGES ON DATABASE school_whatsapp TO school_admin;
```

Update `.env`:
```
DB_ENGINE = django.db.backends.postgresql
DB_NAME = school_whatsapp
DB_USER = school_admin
DB_PASSWORD = your_password
DB_HOST = localhost
DB_PORT = 5432
```

## ============================================================================
## 6. DATABASE MIGRATIONS
## ============================================================================

Run migrations to create database tables:

```bash
python manage.py migrate
```

## ============================================================================
## 7. INITIALIZE APPLICATION
## ============================================================================

Create default admin user and sample templates:

```bash
python manage.py initialize_app
```

This will create:
- Admin user: `admin` / `admin123` (CHANGE THIS IN PRODUCTION!)
- Sample school: "My School"
- 4 sample message templates

## ============================================================================
## 8. RUNNING THE APPLICATION
## ============================================================================

### 8.1 Development Server

Start the development server:

```bash
python manage.py runserver
```

Application will be available at: **http://localhost:8000**

### 8.2 Access the System

1. Open browser and go to: http://localhost:8000
2. Login with: admin / admin123
3. Change password immediately!

### 8.3 Stop Server

Press: `Ctrl + C`

## ============================================================================
## 9. FIRST TIME USE - STEP BY STEP
## ============================================================================

### Step 1: Login
- Username: `admin`
- Password: `admin123`

### Step 2: Upload Contacts
- Go to "Contacts" → "Upload Contacts"
- Prepare Excel file with columns: Name, Phone
- Upload the file
- Select language (English/Telugu)
- Click "Upload Contacts"

### Step 3: Create Message
- Go to "Messages" → "Send New Message"
- Enter title and message content
- Support for English and Telugu
- Click "Save Message"

### Step 4: Send Message
- Go to "Messages"
- Select the message
- Click "Send Message"
- Choose target language
- Messages will be sent via WhatsApp Web

### Step 5: Monitor Progress
- Real-time progress tracking
- View sending logs
- Export reports as CSV

## ============================================================================
## 10. EXCEL FILE FORMAT
## ============================================================================

Your Excel file should look like this:

| Name           | Phone        |
|---|---|
| Rajesh Kumar   | 9876543210   |
| Priya Singh    | 9123456789   |
| Amit Patel     | 919876543210 |

**Rules:**
- First row should contain headers
- Columns: Name, Phone (case-insensitive)
- Phone can be 10-15 digits
- Phone must be numeric only
- No special characters in phone numbers

## ============================================================================
## 11. SECURITY CHECKLIST
## ============================================================================

Before production deployment:

- [ ] Change admin password
- [ ] Update SECRET_KEY in .env
- [ ] Set DEBUG=False in settings.py
- [ ] Configure allowed hosts
- [ ] Setup HTTPS/SSL
- [ ] Enable CSRF protection
- [ ] Setup backup system
- [ ] Configure email notifications
- [ ] Review database access controls
- [ ] Setup monitoring and logging

## ============================================================================
## 12. FEATURES GUIDE
## ============================================================================

### Dashboard
- View statistics
- Recent messages
- Quick actions
- Tips and help

### Contacts Management
- Upload from Excel
- Search and filter
- Multi-language support
- Block/unblock contacts
- Delete individual or bulk

### Message Management
- Create messages
- Schedule sending
- Multi-language support
- View delivery status
- Export reports

### Message Templates
- Predefined templates
- Reusable messages
- English and Telugu
- Quick copy to messages

### Activity Logs
- Admin panel
- All operations logged
- IP address tracking
- Audit trail

## ============================================================================
## 13. TROUBLESHOOTING
## ============================================================================

### QR Code Not Scanning
- Make sure Chrome browser is fully open
- Ensure phone camera is working
- Check internet connection
- Try clearing browser cache

### Messages Not Sending
- Verify WhatsApp Web is working on browser
- Check internet connection
- Ensure phone numbers are valid
- Review activity logs for errors

### Database Errors
- Run migrations: `python manage.py migrate`
- Check database credentials in .env
- Verify database is running

### Port Already in Use
```bash
python manage.py runserver 8001
```

## ============================================================================
## 14. PROJECT STRUCTURE
## ============================================================================

```
school_whatsapp_system/
├── manage.py                          # Django management
├── requirements.txt                   # Python dependencies
├── .env.example                       # Environment template
│
├── school_notification/               # Main Django project
│   ├── settings.py                    # Settings
│   ├── urls.py                        # URL routing
│   ├── wsgi.py                        # WSGI config
│   └── __init__.py
│
└── whatsapp_app/                      # Main application
    ├── models.py                      # Database models
    ├── views.py                       # Views and logic
    ├── forms.py                       # Django forms
    ├── urls.py                        # App URLs
    ├── admin.py                       # Admin config
    ├── whatsapp_sender.py             # Selenium automation
    ├── config.py                      # Configuration
    │
    ├── templates/                     # HTML templates
    │   ├── base.html                  # Base template
    │   ├── login.html
    │   ├── dashboard.html
    │   ├── messages_list.html
    │   ├── contacts_list.html
    │   ├── upload_contacts.html
    │   ├── create_message.html
    │   ├── message_detail.html
    │   ├── templates_list.html
    │   └── create_template.html
    │
    ├── static/                        # Static files
    │   ├── css/
    │   ├── js/
    │   └── uploads/                   # Uploaded files
    │
    ├── migrations/                    # Database migrations
    └── management/commands/           # Custom commands
```

## ============================================================================
## 15. ADDITIONAL INFORMATION
## ============================================================================

### Technologies Used
- **Backend**: Django 4.2
- **Database**: SQLite/PostgreSQL
- **Automation**: Selenium WebDriver
- **Frontend**: Bootstrap 5
- **Data Processing**: Pandas

### Supported Languages
- English
- Telugu
- Extensible for more languages

### Browser Support
- Chrome (Recommended)
- Edge
- Firefox

### Phone Number Support
- 10-15 digit phone numbers
- Support for country codes
- Format: 9876543210 or 919876543210

### Message Limits
- 4096 characters per message
- Support for emojis
- Multi-line messages supported

## ============================================================================
## 16. GETTING HELP
## ============================================================================

### Common Issues

1. **ModuleNotFoundError**
   ```bash
   pip install -r requirements.txt
   ```

2. **Database errors**
   ```bash
   python manage.py migrate
   ```

3. **Static files not loading**
   ```bash
   python manage.py collectstatic
   ```

4. **Port already in use**
   ```bash
   python manage.py runserver 0.0.0.0:8001
   ```

### Check Logs

View application logs:
```bash
# Windows
type whatsapp_app\logs\whatsapp.log

# Linux/Mac
cat whatsapp_app/logs/whatsapp.log
```

## ============================================================================
## 17. PRODUCTION DEPLOYMENT
## ============================================================================

### Using Gunicorn

```bash
pip install gunicorn
gunicorn school_notification.wsgi:application --bind 0.0.0.0:8000
```

### Using Nginx

Configure nginx as reverse proxy for enhanced security and performance.

### Environment Variables for Production

```
SECRET_KEY = [generate-strong-key]
DEBUG = False
ALLOWED_HOSTS = yourdomain.com,www.yourdomain.com
DB_ENGINE = django.db.backends.postgresql
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
```

## ============================================================================
## 18. SUPPORT AND CONTACT
## ============================================================================

For issues, feature requests, or feedback, please contact:
- Email: support@schoolwhatsapp.local
- Phone: [Your Support Number]

---

**Last Updated**: 2024
**Version**: 1.0
**License**: Open Source
