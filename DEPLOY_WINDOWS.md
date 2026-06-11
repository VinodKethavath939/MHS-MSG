# Windows Deployment

This app should be deployed on a machine where Chrome can open and stay logged in to WhatsApp Web. A normal serverless host is not enough for the message sender because Selenium needs a real Chrome session.

## 1. Prepare Environment

Copy `.env.production.example` to `.env`, then update:

- `SECRET_KEY`
- `DEBUG=False`
- `ALLOWED_HOSTS`
- `CSRF_TRUSTED_ORIGINS`
- `CHROME_DRIVER_PATH`

Keep the machine logged in when sending WhatsApp messages, because Chrome must be able to open for QR scanning and message sending.

## 2. Run Deployment

From PowerShell:

```powershell
cd "C:\Users\vinod\Desktop\MHS MSG\school_whatsapp_system"
.\deploy_windows.ps1
```

Open:

```text
http://SERVER-IP:8000
```

## 3. First WhatsApp Send

Log in to the app, send a test message to one number, and scan the QR code in the Chrome window that opens. After that, the Selenium Chrome profile should keep the WhatsApp session.

## 4. Public Access

For a public domain, put IIS, Nginx, Apache, or a reverse proxy in front of Waitress and forward traffic to `127.0.0.1:8000`. Add the domain to `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS`.

Example:

```env
ALLOWED_HOSTS=school.example.com
CSRF_TRUSTED_ORIGINS=https://school.example.com
```

## Important

Do not rely on Vercel or similar serverless hosting for WhatsApp sending. It can host Django pages, but the Selenium Chrome session will not be stable enough for WhatsApp Web automation.
