# DEPLOYMENT & TESTING GUIDE

## Quick Deployment Checklist

### ✅ Pre-Deployment

- [ ] Python 3.9+ installed
- [ ] Google Chrome browser installed
- [ ] ChromeDriver downloaded and path updated in .env
- [ ] All requirements.txt dependencies installed
- [ ] Database migrations completed
- [ ] Admin user created
- [ ] .env file configured
- [ ] Static files collected (for production)

### ✅ Development Testing

#### 1. Start Development Server
```bash
python manage.py runserver
```

Expected output:
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

#### 2. Access Application
Open browser: http://localhost:8000

#### 3. Login Test
- Username: admin
- Password: admin123
- Should redirect to dashboard

#### 4. Upload Contacts Test
1. Go to Contacts → Upload Contacts
2. Download sample_contacts.xlsx from project root
3. Select file and choose "English" language
4. Click Upload
5. Verify: Should show "Imported: 5 contacts"

#### 5. Create Message Test
1. Go to Messages → Send New Message
2. Enter:
   - Title: "Test Message"
   - Message: "This is a test message"
3. Click Save
4. Should redirect to message detail page

#### 6. Message Template Test
1. Go to Templates → Create New Template
2. Enter template data
3. Click Save
4. Verify: Should list on templates page

#### 7. Search & Filter Test
1. Go to Contacts
2. Search by name
3. Filter by language
4. Verify: Results update correctly

### ✅ WhatsApp Automation Testing

#### Manual QR Code Scan Test
```bash
python -c "
from whatsapp_app.whatsapp_sender import WhatsAppSender

sender = WhatsAppSender()
sender.setup_driver()
sender.open_whatsapp_web()
# Scan QR code manually within 60 seconds
input('Press Enter when done...')
sender.close()
"
```

#### Automated Message Send Test
```python
from whatsapp_app.models import BulkMessage, Contact, SchoolSetting
from whatsapp_app.utils import send_bulk_messages_async
from django.contrib.auth.models import User

# Get or create test objects
user = User.objects.get(username='admin')
school = SchoolSetting.objects.get(admin_user=user)
message = BulkMessage.objects.create(
    school=school,
    title='Test Message',
    message_en='Test content',
    created_by=user
)

# Send messages
success = send_bulk_messages_async(message.id, 'en')
print(f"Send result: {success}")
```

### ✅ Database Testing

#### Check Database Structure
```bash
python manage.py dbshell

# SQLite commands
.tables  # List all tables
.schema whatsapp_app_contact  # View table structure
SELECT COUNT(*) FROM whatsapp_app_contact;  # Count records
```

#### Test Database Queries
```bash
python manage.py shell

# In Django shell
from whatsapp_app.models import Contact, BulkMessage
Contact.objects.count()  # Should show total contacts
BulkMessage.objects.count()  # Should show total messages
```

### ✅ API Testing

#### Test Progress API
```bash
# Using curl
curl http://localhost:8000/api/message/1/progress/

# Response should be:
{
    "total": 5,
    "sent": 2,
    "failed": 0,
    "pending": 3,
    "progress": 40,
    "status": "sending"
}
```

#### Test Statistics API
```bash
curl http://localhost:8000/api/contacts/stats/

# Response should be:
{
    "total": 100,
    "english": 60,
    "telugu": 40,
    "blocked": 0,
    "active": 100
}
```

## Testing Scenarios

### Scenario 1: Basic Message Sending
1. Upload 5 contacts
2. Create message
3. Send to English contacts
4. Verify status changes to "sending"
5. Monitor progress bar
6. Check message logs

### Scenario 2: Multi-Language Support
1. Upload contacts with mixed languages
2. Create message with both EN and TE
3. Send to "Both" languages
4. Verify EN contacts get EN message
5. Verify TE contacts get TE message

### Scenario 3: Contact Management
1. Upload 10 contacts
2. Search for specific contact
3. Filter by language
4. Delete one contact
5. Verify count updates

### Scenario 4: Error Handling
1. Upload file with invalid phone numbers
2. System should skip invalid entries
3. Show error count in import summary
4. Test with malformed Excel file
5. Verify graceful error handling

### Scenario 5: Session Persistence
1. Login and send message (use existing session)
2. Restart browser (without logout)
3. Try to send again
4. Should not require QR scan
5. Message should send without browser restart

## Performance Testing

### Load Testing Steps

1. **Create large contact list** (500+ contacts)
   ```bash
   python manage.py shell
   
   from whatsapp_app.models import Contact, SchoolSetting
   from django.contrib.auth.models import User
   
   school = SchoolSetting.objects.get(admin_user__username='admin')
   
   # Create 500 test contacts
   for i in range(500):
       Contact.objects.create(
           name=f'Contact {i}',
           phone=f'98765{i:05d}',
           school=school
       )
   ```

2. **Test search performance**
   ```
   Go to Contacts → Search for "Contact"
   Should load in <2 seconds
   ```

3. **Test bulk send with 100 contacts**
   ```
   Create message for 100 contacts
   Monitor memory usage
   Check if message completes without crash
   ```

4. **Monitor database size**
   ```bash
   ls -lh db.sqlite3
   # Should be <50MB for 1000 contacts and 100 messages
   ```

## Production Deployment

### Pre-Production Checklist

- [ ] Change admin password
- [ ] Update SECRET_KEY in settings
- [ ] Set DEBUG = False
- [ ] Configure ALLOWED_HOSTS
- [ ] Setup HTTPS/SSL certificate
- [ ] Configure PostgreSQL database
- [ ] Enable CSRF protection
- [ ] Configure logging to file
- [ ] Setup email backend
- [ ] Configure backup strategy
- [ ] Test error pages (404, 500)

### Production Server Setup

1. **Install production server (Gunicorn)**
   ```bash
   pip install gunicorn
   ```

2. **Create systemd service file** (/etc/systemd/system/whatsapp-app.service)
   ```ini
   [Unit]
   Description=School WhatsApp Notification System
   After=network.target
   
   [Service]
   Type=notify
   User=www-data
   WorkingDirectory=/path/to/app
   Environment="PATH=/path/to/venv/bin"
   ExecStart=/path/to/venv/bin/gunicorn \
       school_notification.wsgi:application \
       --workers 4 \
       --bind unix:/path/to/app/wsgi.sock
   
   [Install]
   WantedBy=multi-user.target
   ```

3. **Configure Nginx**
   ```nginx
   upstream django {
       server unix:/path/to/app/wsgi.sock;
   }
   
   server {
       listen 443 ssl http2;
       server_name yourdomain.com;
       
       ssl_certificate /path/to/cert.crt;
       ssl_certificate_key /path/to/key.key;
       
       location /static {
           alias /path/to/app/staticfiles/;
       }
       
       location /media {
           alias /path/to/app/media/;
       }
       
       location / {
           proxy_pass http://django;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

4. **Run migrations on production**
   ```bash
   python manage.py migrate --noinput
   python manage.py collectstatic --noinput
   ```

5. **Start services**
   ```bash
   systemctl start whatsapp-app
   systemctl enable whatsapp-app
   systemctl start nginx
   systemctl enable nginx
   ```

## Monitoring & Troubleshooting

### Monitor Logs
```bash
# Django logs
tail -f whatsapp_app/logs/whatsapp.log

# System logs
journalctl -u whatsapp-app -f

# Nginx logs
tail -f /var/log/nginx/error.log
```

### Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| QR Code Not Scanning | Ensure Chrome is fully loaded, try incognito mode, check internet |
| Messages Not Sending | Verify phone numbers format, check WhatsApp Web manually, review logs |
| Database Lock | Restart application, check for long-running queries |
| High Memory Usage | Reduce worker count, restart Gunicorn, check for memory leaks |
| Static Files Not Loading | Run collectstatic, check nginx configuration |

## Rollback Procedure

If deployment fails:

```bash
# Revert database
python manage.py migrate 0001_initial  # Go back to first migration

# Or restore from backup
psql -d school_whatsapp < backup.sql

# Restart application
systemctl restart whatsapp-app
```

## Performance Optimization Tips

1. **Enable caching**
   - Redis for session storage
   - Cache contact statistics

2. **Database optimization**
   - Add indexes on frequently searched fields
   - Archive old message logs

3. **Frontend optimization**
   - Minify CSS/JS
   - Enable gzip compression
   - Use CDN for static files

4. **Async message sending**
   - Use Celery for background tasks
   - Process long-running operations asynchronously

## Security Audit Checklist

- [ ] SQL injection prevention (use ORM)
- [ ] XSS prevention (template escaping)
- [ ] CSRF protection enabled
- [ ] Sensitive data not logged
- [ ] Password requirements enforced
- [ ] Rate limiting on login
- [ ] Secure cookies settings
- [ ] Regular backup system
- [ ] Access logs monitored
- [ ] Security headers configured

---

**Last Updated:** 2024
**Version:** 1.0
