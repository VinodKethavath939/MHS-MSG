# QUICK REFERENCE CARD

## 🚀 QUICK START (60 seconds)

```bash
# 1. Navigate to project
cd school_whatsapp_system

# 2. Create virtual environment
python -m venv venv

# 3. Activate (Windows) or source venv/bin/activate (Linux/Mac)
venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run migrations
python manage.py migrate

# 6. Initialize app (creates admin user)
python manage.py initialize_app

# 7. Start server
python manage.py runserver

# 8. Open browser
http://localhost:8000

# 9. Login
Username: admin
Password: admin123
```

---

## 📱 USER QUICK GUIDE

### Upload Contacts
1. Contacts → Upload Contacts
2. Select Excel file (Name, Phone columns)
3. Choose language (English/Telugu)
4. Click Upload

### Send Messages
1. Messages → Send New Message
2. Enter title and message
3. Click Save
4. Click Send → Choose language → Start sending

### Monitor Progress
- Real-time progress bar
- View sent/failed count
- Check individual logs
- Export report as CSV

---

## 💻 DEVELOPER COMMANDS

```bash
# Database
python manage.py migrate                    # Run migrations
python manage.py makemigrations             # Create migrations
python manage.py dbshell                    # Open database shell
python manage.py shell                      # Open Python shell

# Admin
python manage.py createsuperuser            # Create admin user
python manage.py changepassword admin       # Change password
python manage.py initialize_app             # Initialize app

# Server
python manage.py runserver                  # Start dev server
python manage.py runserver 0.0.0.0:8000    # Bind to all IPs
python manage.py collectstatic              # Collect static files

# Testing
python manage.py test                       # Run tests
python manage.py test whatsapp_app         # Test specific app

# Other
python manage.py flush                      # Clear database
python manage.py dumpdata > backup.json    # Backup database
python manage.py loaddata backup.json      # Restore database
```

---

## 📁 IMPORTANT FILES

| File | Purpose |
|------|---------|
| `manage.py` | Django management |
| `settings.py` | Configuration |
| `models.py` | Database models |
| `views.py` | Request handlers |
| `forms.py` | Form definitions |
| `urls.py` | URL routing |
| `whatsapp_sender.py` | Selenium automation |
| `.env` | Environment variables |
| `requirements.txt` | Dependencies |

---

## 🔑 DEFAULT CREDENTIALS

```
Username: admin
Password: admin123
Email: admin@school.local
```

⚠️ **CHANGE PASSWORD IMMEDIATELY!**

---

## 🌐 URL ROUTES

| URL | Purpose |
|-----|---------|
| `/` | Login page |
| `/dashboard/` | Dashboard |
| `/contacts/` | Contacts list |
| `/contacts/upload/` | Upload contacts |
| `/messages/` | Messages list |
| `/messages/create/` | Create message |
| `/messages/{id}/` | Message detail |
| `/templates/` | Message templates |
| `/api/message/{id}/progress/` | Progress API |
| `/api/contacts/stats/` | Stats API |
| `/admin/` | Django admin |

---

## 📊 DATABASE MODELS QUICK VIEW

```
SchoolSetting
├─ school_name
├─ admin_user (ForeignKey → User)
└─ logo (Image)

Contact
├─ name
├─ phone (Unique per school)
├─ email
├─ language (EN/TE)
├─ is_blocked
└─ school (ForeignKey)

BulkMessage
├─ title
├─ message_en, message_te
├─ status (DRAFT/SCHEDULED/SENDING/COMPLETED/FAILED)
├─ total_contacts
├─ sent_count, failed_count
├─ scheduled_time
└─ school (ForeignKey)

MessageLog
├─ bulk_message (ForeignKey)
├─ contact (ForeignKey)
├─ status (PENDING/SENT/FAILED/BLOCKED)
├─ error_message
└─ timestamps

ActivityLog
├─ admin_user (ForeignKey)
├─ action (LOGIN/LOGOUT/UPLOAD/SEND/DELETE/EXPORT)
├─ description
├─ ip_address
└─ timestamp

HolidayTemplate
├─ name
├─ message_en, message_te
├─ school (ForeignKey)
└─ timestamps
```

---

## 🔧 COMMON TASKS

### Create Superuser
```bash
python manage.py createsuperuser
```

### Reset Database
```bash
python manage.py flush
python manage.py migrate
```

### Test WhatsApp Sender
```python
from whatsapp_app.whatsapp_sender import WhatsAppSender

sender = WhatsAppSender()
sender.setup_driver()
sender.open_whatsapp_web()  # Scan QR code
# Test complete!
sender.close()
```

### Test Message Sending
```python
from whatsapp_app.utils import send_bulk_messages_async

# Send message ID 1 to English contacts
send_bulk_messages_async(message_id=1, target_language='en')
```

### Get Statistics
```python
from whatsapp_app.utils import get_message_statistics

stats = get_message_statistics(message_id=1)
print(stats)
# Output: {sent: 10, failed: 2, pending: 3, ...}
```

---

## 🐛 TROUBLESHOOTING

| Issue | Solution |
|-------|----------|
| ModuleNotFoundError | `pip install -r requirements.txt` |
| Database Error | `python manage.py migrate` |
| Static Files Not Loading | `python manage.py collectstatic` |
| QR Code Not Scanning | Check Chrome, try incognito mode |
| Messages Not Sending | Verify phone numbers, check WhatsApp Web manually |
| Port Already in Use | `python manage.py runserver 8001` |
| Chrome Not Found | Install Chrome from google.com/chrome/ |
| ChromeDriver Not Working | Download matching version from chromedriver.org |

---

## 📄 EXCEL FILE FORMAT

**Required Columns:**
- Name
- Phone

**Example:**
```
| Name           | Phone        |
|---|---|
| Rajesh Kumar   | 9876543210   |
| Priya Singh    | 919123456789 |
```

**Rules:**
- Headers: Name, Phone (case-insensitive)
- Phone: 10-15 digits only
- Max file size: 5MB
- Formats: .xlsx, .xls, .csv

---

## 🌍 LANGUAGE CODES

| Language | Code |
|----------|------|
| English | en |
| Telugu | te |

---

## 📈 MESSAGE STATUS FLOW

```
DRAFT → SCHEDULED → SENDING → COMPLETED/FAILED
                   ↓
              (Auto-save progress)
```

---

## 🔐 SECURITY TIPS

- ✅ Change default admin password
- ✅ Use strong passwords (min 12 chars, mix case, numbers, symbols)
- ✅ Keep Django & packages updated
- ✅ Enable HTTPS in production
- ✅ Review activity logs regularly
- ✅ Backup database regularly
- ✅ Restrict file uploads
- ✅ Monitor disk space

---

## 📞 CONTACT INFO

**For Issues:**
- Check SETUP_GUIDE.md
- Review TECHNICAL_DOCUMENTATION.md
- Check logs: `whatsapp_app/logs/whatsapp.log`
- Review code comments in problematic file

---

## 📚 DOCUMENTATION MAP

| Document | Purpose |
|----------|---------|
| README.md | Overview & features |
| SETUP_GUIDE.md | Installation steps |
| TECHNICAL_DOCUMENTATION.md | Architecture & API |
| DEPLOYMENT_TESTING_GUIDE.md | Testing & deployment |
| PROJECT_COMPLETION_SUMMARY.md | Full deliverables |
| This file | Quick reference |

---

## 🎯 PERFORMANCE TIPS

- Batch messages (50-100 at a time)
- Use 2-second delay between messages
- Monitor browser memory
- Restart server weekly
- Archive old message logs
- Use PostgreSQL for 1000+ contacts
- Enable Redis for caching
- Implement Celery for async tasks

---

## 💾 BACKUP & RESTORE

### Backup Database
```bash
python manage.py dumpdata > backup.json
```

### Restore Database
```bash
python manage.py loaddata backup.json
```

### Backup Files
```bash
# Backup uploads directory
cp -r whatsapp_app/static/uploads/ backup/uploads/

# Backup database
cp db.sqlite3 backup/db.sqlite3
```

---

## 🔄 UPDATE DEPENDENCIES

```bash
pip install -r requirements.txt --upgrade
pip freeze > requirements.txt  # Update with latest versions
```

---

## 🚀 PRODUCTION CHECKLIST

- [ ] Change SECRET_KEY
- [ ] Set DEBUG = False
- [ ] Update ALLOWED_HOSTS
- [ ] Configure database (PostgreSQL)
- [ ] Setup email backend
- [ ] Enable HTTPS/SSL
- [ ] Configure firewall
- [ ] Setup backup system
- [ ] Enable monitoring
- [ ] Configure logging
- [ ] Test error pages
- [ ] Security headers enabled
- [ ] CSRF protection on
- [ ] Database indexed
- [ ] Load tested
- [ ] Documented runbooks

---

## 📱 MOBILE ACCESS

The system is fully responsive:
- Works on tablets
- Works on mobile devices
- Touch-friendly buttons
- Optimized layouts

---

## 🎓 TRAINING NOTES

### For Admins
- Login only with provided credentials
- Upload contacts before sending messages
- Monitor message progress
- Export reports for records
- Change password monthly

### For Developers
- Follow Django best practices
- Comment your code
- Write tests for new features
- Update documentation
- Review security implications

---

## ⚡ PERFORMANCE METRICS

- Page load: < 2 seconds
- Contact search: < 1 second
- Message creation: < 1 second
- Report export: < 5 seconds (1000 records)
- Message send: 2 seconds per contact (with delay)

---

## 📋 CHECKLIST FOR FIRST RUN

- [ ] Python 3.9+ installed
- [ ] Chrome browser installed
- [ ] ChromeDriver downloaded
- [ ] Requirements installed
- [ ] Database migrated
- [ ] App initialized
- [ ] Admin password changed
- [ ] .env configured
- [ ] Server running
- [ ] Can login
- [ ] Can upload contacts
- [ ] Can create message
- [ ] Can scan WhatsApp QR
- [ ] Test message sent successfully

---

**Version**: 1.0 | **Last Updated**: 2024 | **Language**: English

