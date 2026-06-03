# School WhatsApp Notification System - README

## 🎓 Professional School WhatsApp Notification System

A complete, production-ready Django application for sending bulk WhatsApp messages to parents and students using WhatsApp Web automation.

### ✨ Features

#### **Admin Dashboard**
- 🔐 Secure login system for administrators
- 📊 Real-time statistics and analytics
- 🎨 Modern, responsive UI with Bootstrap 5
- 📱 Mobile-friendly design

#### **Contact Management**
- 📥 Upload contacts from Excel/CSV files
- 🔍 Search and filter contacts by name/phone
- 🌐 Multi-language support (English & Telugu)
- 📋 Bulk contact management
- 🚫 Block/unblock contacts

#### **Message Management**
- ✉️ Create and schedule messages
- 🌍 Multi-language message support
- 📅 Message scheduling feature
- 📊 Real-time progress tracking
- 📈 Detailed delivery reports
- 🔄 Message retry mechanism

#### **WhatsApp Automation**
- 🤖 Selenium-based WhatsApp Web automation
- 🔐 Secure QR code session management
- ⚡ Bulk sending support for 800+ contacts
- ⏱️ Intelligent delay system to avoid blocking
- 🛡️ Error handling and recovery
- 📝 Comprehensive logging

#### **Reports & Analytics**
- 📊 Real-time message delivery status
- 💾 Export reports as CSV
- 📈 Detailed activity logs
- 👤 Admin audit trail with IP tracking

#### **Message Templates**
- 📄 Pre-defined holiday templates
- 🎯 Reusable message templates
- 🌐 Multi-language template support
- ⚡ Quick message creation

### 🛠️ Technology Stack

```
Backend:        Django 4.2
Database:       SQLite (dev) / PostgreSQL (prod)
Automation:     Selenium WebDriver
Frontend:       Bootstrap 5, HTML5, CSS3, JavaScript
Data Processing: Pandas
Web Server:     Gunicorn (production)
Task Queue:     Celery (optional)
Cache:          Redis (optional)
```

### 📋 System Requirements

- **Python**: 3.9 or higher
- **RAM**: 2GB minimum (4GB recommended)
- **Storage**: 500MB minimum
- **OS**: Windows, Linux, macOS
- **Browser**: Google Chrome (latest version)
- **Internet**: 24/7 connection for messages

### 🚀 Quick Start

#### 1. Setup Environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### 2. Configure Database

```bash
# Run migrations
python manage.py migrate

# Initialize app (creates admin user and templates)
python manage.py initialize_app
```

#### 3. Setup ChromeDriver

- Download from: https://chromedriver.chromium.org/downloads
- Extract and note the path
- Update `.env` file with path

#### 4. Run Application

```bash
python manage.py runserver
```

Open: http://localhost:8000

#### 5. Login

- **Username**: admin
- **Password**: admin123
- **⚠️ Change password immediately!**

### 📝 Excel File Format

Your contact Excel file must have:

```
| Name           | Phone        |
|---|---|
| Rajesh Kumar   | 9876543210   |
| Priya Singh    | 9123456789   |
```

**Rules:**
- Headers: Name, Phone (case-insensitive)
- Phone: 10-15 digits
- Supports formats: 9876543210 or 919876543210

### 📖 Usage Guide

#### Uploading Contacts

1. Go to **Contacts → Upload Contacts**
2. Select Excel file with Name and Phone columns
3. Choose default language (English/Telugu)
4. Check "Overwrite" if updating existing contacts
5. Click "Upload Contacts"

#### Creating Messages

1. Go to **Messages → Send New Message**
2. Enter message title
3. Type message in English (required) and Telugu (optional)
4. Optionally set schedule date/time
5. Click "Save Message"

#### Sending Messages

1. Go to **Messages**
2. Click on your message
3. Choose target language (English/Telugu/Both)
4. Click "Send Message"
5. **Browser will open WhatsApp Web**
6. **Scan QR code on first login**
7. **Messages will send automatically**

#### Monitoring Progress

- Real-time progress bar during sending
- View sent/failed/pending count
- Click "View Details" for individual logs
- Export report as CSV when completed

#### Using Templates

1. Go to **Templates**
2. Click "Create New Template"
3. Enter template name and messages
4. When creating messages, click template to use it
5. Customize and send

### 🔒 Security Features

✅ Admin authentication required
✅ Session security with CSRF protection
✅ Secure password hashing
✅ Activity logging with IP tracking
✅ Duplicate message prevention
✅ Phone number validation
✅ Secure file upload handling

### 📊 Database Models

#### Contact
- Name, Phone, Email
- Language preference (English/Telugu)
- Block status
- Created/Updated timestamps

#### BulkMessage
- Title, Message content (EN/TE)
- Status (Draft/Scheduled/Sending/Completed)
- Scheduling information
- Delivery statistics

#### MessageLog
- Track individual message delivery
- Status and error messages
- Retry attempts
- Timestamps

#### ActivityLog
- All admin actions logged
- Login/Logout tracking
- File uploads
- Message sending
- IP address recording

#### HolidayTemplate
- Reusable message templates
- English and Telugu versions
- Easy to customize and reuse

### 🐛 Troubleshooting

#### QR Code Not Displaying
```
- Ensure Chrome browser opens automatically
- Check internet connection
- Try using Chrome in incognito mode
```

#### Messages Not Sending
```
- Verify WhatsApp Web works on browser manually
- Check phone numbers are valid
- Review logs in whatsapp_app/logs/
- Ensure internet connection is stable
```

#### Database Errors
```bash
python manage.py migrate
python manage.py migrate --run-syncdb
```

#### Module Not Found
```bash
pip install -r requirements.txt --upgrade
```

### 📁 Project Structure

```
school_whatsapp_system/
├── manage.py
├── requirements.txt
├── .env.example
├── SETUP_GUIDE.md
├── README.md
│
├── school_notification/          # Django project
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│
└── whatsapp_app/                 # Main app
    ├── models.py                 # Database models
    ├── views.py                  # View logic
    ├── forms.py                  # Forms
    ├── urls.py                   # URL routing
    ├── whatsapp_sender.py        # Selenium automation
    ├── admin.py                  # Admin interface
    ├── config.py                 # Configuration
    │
    ├── templates/                # HTML templates
    │   ├── base.html
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
    ├── static/
    │   ├── css/
    │   ├── js/
    │   └── uploads/
    │
    ├── migrations/
    └── management/commands/
```

### 🎯 Key Features Explained

#### **Bulk Message Sending**
- Sends 800+ messages in a single campaign
- Automatic delays between messages (2 seconds)
- Prevents WhatsApp account blocking
- Retry failed messages automatically

#### **Multi-Language Support**
- Send different messages based on language preference
- English and Telugu built-in
- Extensible for more languages
- Fallback to default language if not available

#### **Session Management**
- WhatsApp session persists between logins
- No need to scan QR code every time
- Session stored securely on device
- Auto-logout after inactivity

#### **Real-Time Progress**
- Live status updates while sending
- Progress bar with percentage
- Sent/Failed/Pending count
- Detailed log for each contact

### 🔑 Admin Credentials (Default)

```
Username: admin
Password: admin123
```

**⚠️ IMPORTANT: Change password after first login!**

### 📦 Dependencies

See `requirements.txt` for all packages. Key ones:
- django==4.2.7
- selenium==4.14.0
- pandas==2.1.1
- openpyxl==3.1.2
- bootstrap==5.3.0 (via CDN)

### 🌍 Multi-Language Example

#### English
"Dear Parents, School will remain closed for holidays. Regular classes will resume on 15th January."

#### Telugu
"ప్రియ తల్లిదండ్రులు, విద్యాలయం ఛుట్టీలకు మూసి ఉంటుంది. సాధారణ తరగతులు 15th జనవరిలో తిరిగి ప్రారంభమవుతాయి."

### 💡 Tips & Best Practices

✅ **Batch Sending**
- Send 50-100 messages at a time for better reliability
- Space out batches by a few hours
- Monitor delivery status after each batch

✅ **Message Content**
- Keep messages concise (200-300 characters)
- Use clear, professional language
- Include important dates and times
- Avoid special characters that WhatsApp doesn't support

✅ **Contact Management**
- Keep contact list clean and updated
- Remove invalid phone numbers
- Block blocked contacts to avoid retry
- Regular backup of contact list

✅ **Security**
- Change admin password regularly
- Use strong, unique passwords
- Review activity logs weekly
- Enable browser notifications for alerts

### 📞 Support & Contact

For issues or feature requests:
- Check SETUP_GUIDE.md for detailed setup instructions
- Review logs in `whatsapp_app/logs/whatsapp.log`
- Check Django error messages in console
- Verify all prerequisites are installed

### 📄 License

This system is provided for educational and school management purposes.

### 🔄 Version History

**v1.0** (2024)
- Initial release
- Django 4.2 framework
- Selenium WhatsApp automation
- Multi-language support
- Full admin dashboard
- Real-time progress tracking

---

**Made with ❤️ for Schools**

Empowering schools with modern communication technology.

Last Updated: 2024 | Version: 1.0
