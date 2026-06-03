# School WhatsApp Notification System - Technical Documentation

## Architecture Overview

The School WhatsApp Notification System follows a modular Django architecture with the following components:

### High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                  Web Browser / Client                    │
│                    (Bootstrap UI)                        │
└────────────────────────┬────────────────────────────────┘
                         │
                    HTTP/HTTPS
                         │
┌────────────────────────▼────────────────────────────────┐
│              Django Application Server                    │
├─────────────────────────────────────────────────────────┤
│  Views & Forms  │  Models  │  Admin Panel  │  APIs      │
└────────────────────────┬────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
    Database        File Storage      Selenium
   (SQLite/        (Uploads)         WebDriver
   PostgreSQL)                       (Chrome)
                                       │
                                       ▼
                                  WhatsApp Web
                                   (Web.whatsapp.com)
```

## Core Components

### 1. Database Models

#### Contact Model
```python
class Contact:
    - id: Primary Key
    - name: CharField(255)
    - phone: CharField(15) - Unique per school
    - email: EmailField - Optional
    - language: Choice(EN/TE)
    - is_blocked: Boolean
    - school: ForeignKey(SchoolSetting)
    - created_at, updated_at: DateTime
```

**Relationships:**
- Many Contacts per School
- One School per Admin User

#### BulkMessage Model
```python
class BulkMessage:
    - id: Primary Key
    - school: ForeignKey(SchoolSetting)
    - title: CharField(255)
    - message_en: TextField
    - message_te: TextField (Optional)
    - status: Choice(DRAFT/SCHEDULED/SENDING/COMPLETED/FAILED)
    - total_contacts: IntegerField
    - sent_count: IntegerField
    - failed_count: IntegerField
    - scheduled_time: DateTime (Optional)
    - created_by: ForeignKey(User)
    - created_at, updated_at, started_at, completed_at: DateTime
```

**Status Flow:**
```
DRAFT → SCHEDULED → SENDING → COMPLETED/FAILED
```

#### MessageLog Model
```python
class MessageLog:
    - id: Primary Key
    - bulk_message: ForeignKey(BulkMessage)
    - contact: ForeignKey(Contact)
    - status: Choice(PENDING/SENT/FAILED/BLOCKED)
    - error_message: TextField (Optional)
    - attempt_count: IntegerField
    - last_attempted_at: DateTime
    - sent_at: DateTime
    - created_at: DateTime
```

**Unique Constraint:** One log per (bulk_message, contact)

### 2. Views & Request Handling

#### Authentication Views
- `login_view`: Admin login with session management
- `logout_view`: Secure logout with activity logging

#### Dashboard Views
- `dashboard`: Statistics and recent messages overview
- Shows total contacts, messages, sent count, pending

#### Contact Management Views
- `contacts_list`: Search, filter, and pagination
- `upload_contacts`: Excel file parsing and bulk import
- `delete_contacts`: Single or bulk deletion

#### Message Management Views
- `messages_list`: All messages with status and progress
- `create_message`: Form for new message creation
- `message_detail`: View logs, status, and export reports
- `send_message`: Initiate bulk sending process

#### API Views
- `api_message_progress`: JSON endpoint for progress tracking
- `api_contacts_stats`: Contact statistics API

### 3. WhatsApp Automation (Selenium)

#### WhatsAppSender Class

**Initialization:**
```python
sender = WhatsAppSender(chrome_driver_path='chromedriver.exe')
```

**Key Methods:**

1. **setup_driver()**
   - Initializes Chrome WebDriver
   - Configures options (session persistence, notifications disabled)
   - Uses user-data-dir for session saving

2. **open_whatsapp_web()**
   - Opens https://web.whatsapp.com
   - Waits for QR code (first login)
   - Waits for chat list (already logged in)
   - Handles both scenarios automatically

3. **search_and_open_contact(phone_number)**
   - Searches contact by phone number
   - Opens chat with contact
   - Formats phone with country code (default +91 for India)

4. **send_message(message, retry_count=3)**
   - Types message in chat box
   - Clicks send button
   - Retries up to 3 times on failure
   - Returns True/False

5. **send_bulk_message(contacts, message, delay=2, progress_callback=None)**
   - Iterates through contact list
   - Calls search_and_open_contact() and send_message() for each
   - Applies delay between messages (avoids blocking)
   - Calls progress_callback() for real-time updates
   - Returns dict with {sent: [], failed: []}

**Error Handling:**
```
TimeoutException → Retry or mark as failed
NoSuchElementException → Element not found, retry
StaleElementReferenceException → Element became stale, retry
General Exception → Log and mark as failed
```

**Session Management:**
```
User Data Dir: C:\Users\[USERNAME]\AppData\Local\WhatsAppSelenium
├── Default/
│   ├── Session Storage/
│   ├── Cookies/
│   └── IndexedDB/
```

### 4. Forms & Data Processing

#### ContactUploadForm
- File validation (extension, size)
- Excel/CSV parsing via pandas
- Phone number validation (10-15 digits)
- Duplicate handling (skip or overwrite)

#### ExcelHelper
```python
validate_and_parse_excel(file_obj)
  → Returns (success, data/error)
  
import_contacts(file_obj, school, language, overwrite)
  → Returns (success, message, stats)
```

### 5. Security Measures

#### Authentication
- Django's built-in User authentication
- Password hashing with PBKDF2
- Session-based authentication
- Login required decorator on views

#### Authorization
- School-level data isolation
- Users can only see their school's data
- Admin-only operations protected

#### CSRF Protection
- CSRF tokens on all forms
- Middleware enabled by default

#### Input Validation
- Form validation on client and server
- File upload validation
- Phone number format validation
- Message length validation (max 4096 chars)

#### Logging & Auditing
- ActivityLog for all operations
- IP address tracking
- User action recording
- Database query logging

### 6. Data Flow: Message Sending

```
┌─────────────────────────┐
│   Create Message        │
│ (title, messages)       │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│  Save as DRAFT          │
│  BulkMessage created    │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│  Select Language        │
│  Get Contacts           │
│  Create MessageLogs     │
│  Set status=SENDING     │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│  Initialize Selenium    │
│  Open WhatsApp Web      │
│  Scan QR (if needed)    │
└────────────┬────────────┘
             │
             ▼
┌──────────────────────────────┐
│  For each Contact:           │
│  ├─ Search & Open chat       │
│  ├─ Send message             │
│  ├─ Update MessageLog status │
│  ├─ Apply 2-second delay     │
│  └─ Progress callback        │
└────────────┬─────────────────┘
             │
             ▼
┌──────────────────────────┐
│  Update BulkMessage      │
│  Set status=COMPLETED    │
│  Record completion time  │
│  Log final statistics    │
└──────────────────────────┘
```

### 7. Real-Time Progress Updates

#### Client-Side (JavaScript)
```javascript
// Auto-refresh every 5 seconds
setInterval(() => {
    fetch(/api/message/{id}/progress/)
    .then(response => response.json())
    .then(data => {
        updateProgressBar(data.progress);
        updateCounts(data.sent, data.failed, data.pending);
    });
}, 5000);
```

#### Server-Side (Django)
```python
@api_view(['GET'])
def api_message_progress(request, message_id):
    message = BulkMessage.objects.get(id=message_id)
    logs = MessageLog.objects.filter(bulk_message=message)
    
    return JsonResponse({
        'total': message.total_contacts,
        'sent': logs.filter(status='sent').count(),
        'failed': logs.filter(status='failed').count(),
        'progress': (sent + failed) / total * 100
    })
```

### 8. Multi-Language Support

#### Language Selection Flow
```
User selects 'en' (English):
├─ Get Contacts where language='en'
├─ Use message.message_en
└─ Send to those contacts

User selects 'te' (Telugu):
├─ Get Contacts where language='te'
├─ Use message.message_te
└─ Send to those contacts

User selects 'both':
├─ Get all Contacts
├─ For language='en' contacts → Use message_en
├─ For language='te' contacts → Use message_te
└─ Send appropriate message to each group
```

## Configuration & Settings

### Environment Variables (.env)

```
# Django
SECRET_KEY = [random-secure-key]
DEBUG = True (dev) / False (prod)

# Database
DB_ENGINE = django.db.backends.sqlite3
DB_NAME = db.sqlite3

# WhatsApp
CHROME_DRIVER_PATH = /path/to/chromedriver
WHATSAPP_MESSAGE_DELAY = 2  (seconds)
WHATSAPP_TIMEOUT = 60  (seconds)

# Email (optional)
EMAIL_BACKEND = django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST = smtp.gmail.com
EMAIL_PORT = 587
```

### Django Settings

```python
# settings.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'whatsapp_app',  # Custom app
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}
```

## Performance Considerations

### Database Optimization
- Indexed fields: phone (Contact), bulk_message_id (MessageLog)
- Unique together: (phone, school) on Contact
- Pagination: 20 items per page on list views

### Message Sending Optimization
```
Contact Load: 100-200 contacts in memory
Delay Strategy: 2 seconds between messages
Batch Size: Send in batches of 50-100
Retry Logic: Up to 3 attempts per contact
```

### Caching (Future Enhancement)
```python
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)  # Cache for 15 minutes
def api_contacts_stats(request):
    ...
```

## Scalability

### Current Capacity
- Up to 800+ contacts per message
- Multiple concurrent messages (with browser sessions)
- SQLite suitable for 1000+ records

### For Growth
- PostgreSQL for large datasets
- Celery for async task processing
- Redis for caching and sessions
- Multiple Selenium instances (with proxies)
- Message queue system

## Error Handling & Recovery

### Common Error Scenarios

1. **QR Code Not Scanning**
   - Timeout after 60 seconds
   - User intervention required
   - Log error with timestamp

2. **Contact Not Found**
   - Log as "failed" status
   - Record error message
   - Mark for retry

3. **Network Interruption**
   - Catch exception and retry
   - After 3 retries, mark as failed
   - Log for manual review

4. **Browser Crash**
   - Exception caught
   - Driver closed safely
   - Message marked as incomplete
   - Can restart later

## Testing

### Unit Tests (to be added)
```python
# tests/test_models.py
def test_contact_creation():
    ...

def test_message_sending():
    ...
```

### Integration Tests
- Excel file parsing
- Contact import workflow
- Message sending workflow

### Manual Testing
- QR code scanning
- Message delivery verification
- Progress tracking accuracy

## Deployment

### Development
```bash
python manage.py runserver
```

### Production (Gunicorn)
```bash
gunicorn school_notification.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 4 \
  --timeout 120
```

### With Nginx (Reverse Proxy)
```nginx
upstream django {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name yourdomain.com;
    
    location / {
        proxy_pass http://django;
        proxy_set_header Host $host;
    }
    
    location /static {
        alias /path/to/staticfiles/;
    }
}
```

## Monitoring & Logging

### Log Files
```
whatsapp_app/logs/whatsapp.log
├── INFO: General operations
├── ERROR: Failures and exceptions
└── DEBUG: Detailed execution
```

### Metrics to Monitor
- Message send success rate
- Average delivery time
- Failed contacts
- User activity
- Database size
- Disk space

## Future Enhancements

1. **Async Task Processing**
   - Celery with Redis
   - Background message sending
   - Scheduled delivery

2. **Advanced Analytics**
   - Delivery charts
   - Success rate trends
   - Contact engagement

3. **Additional Languages**
   - Hindi, Marathi, Kannada, etc.
   - Right-to-left language support

4. **Group Messaging**
   - WhatsApp groups
   - Group management
   - Broadcast lists

5. **Media Support**
   - Image attachments
   - Document sending
   - Voice messages

6. **Webhook Integration**
   - WhatsApp Business API
   - Real-time delivery reports
   - Two-way messaging

---

**Document Version:** 1.0
**Last Updated:** 2024
**Maintainer:** School WhatsApp Team
