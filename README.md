# Simple Law Firm Website

A beginner-friendly Flask website with a responsive pastel sage/cream design, WhatsApp links, and an email enquiry form.

## 1. Requirements
- Python 3.9 or newer
- Internet connection for the optional Google Fonts and Unsplash hero image

## 2. Run locally
1. Extract this ZIP folder.
2. Open a terminal/command prompt inside `simple_law_firm_website`.
3. Install Flask:
   `python -m pip install flask`
4. Set your contact settings (see below).
5. Start the app:
   `python app.py`
6. Open `http://127.0.0.1:5000`.

## 3. Configure WhatsApp
The default WhatsApp number is deliberately a placeholder. Set `WHATSAPP_NUMBER` to the firm's WhatsApp number in international digits only, without a plus sign, spaces or dashes. Example format: `27821234567`.

Windows PowerShell (current terminal session):
```powershell
$env:WHATSAPP_NUMBER="27821234567"
python app.py
```

macOS/Linux:
```bash
export WHATSAPP_NUMBER="27821234567"
python app.py
```

## 4. Configure email delivery
The form saves enquiries to `enquiries.json` and attempts to email the firm using SMTP. Email will not be delivered until valid SMTP settings are configured.

Set these environment variables:
- `SMTP_HOST` — SMTP server hostname from your email provider
- `SMTP_PORT` — usually `587` for STARTTLS
- `SMTP_USERNAME` — SMTP login username
- `SMTP_PASSWORD` — SMTP password or provider-issued app password
- `ENQUIRY_TO_EMAIL` — the firm's destination inbox
- `ENQUIRY_FROM_EMAIL` — sender address accepted by your provider (often the same as SMTP_USERNAME)
- `FLASK_SECRET_KEY` — a long, random secret for Flask sessions

Windows PowerShell example (use your actual provider values):
```powershell
$env:SMTP_HOST="smtp.example.com"
$env:SMTP_PORT="587"
$env:SMTP_USERNAME="website@example.co.za"
$env:SMTP_PASSWORD="YOUR_PROVIDER_APP_PASSWORD"
$env:ENQUIRY_TO_EMAIL="info@example.co.za"
$env:ENQUIRY_FROM_EMAIL="website@example.co.za"
$env:FLASK_SECRET_KEY="replace-with-a-long-random-secret"
$env:WHATSAPP_NUMBER="27821234567"
python app.py
```

macOS/Linux example:
```bash
export SMTP_HOST="smtp.example.com"
export SMTP_PORT="587"
export SMTP_USERNAME="website@example.co.za"
export SMTP_PASSWORD="YOUR_PROVIDER_APP_PASSWORD"
export ENQUIRY_TO_EMAIL="info@example.co.za"
export ENQUIRY_FROM_EMAIL="website@example.co.za"
export FLASK_SECRET_KEY="replace-with-a-long-random-secret"
export WHATSAPP_NUMBER="27821234567"
python app.py
```

Use the SMTP hostname and credentials from your actual email provider; `smtp.example.com` is only a placeholder. Many providers require an app password or authenticated SMTP access. Never put real passwords in source code or commit them to version control.

## 5. Important before publishing
- Replace `Nkosi & Partners`, the placeholder email/phone details, and example services.
- Set the correct WhatsApp number and SMTP settings.
- Run behind a production WSGI server with HTTPS; do not use Flask's development server for public traffic.
- Add appropriate privacy, POPIA, and legal notices after getting suitable professional advice.
- Enquiries contain personal information. The demo writes submissions to a local JSON file; secure access, backups, retention, spam protection, rate limiting and privacy compliance need to be addressed before public deployment.
- The app attempts email delivery after saving. If email is not configured or delivery fails, it shows a notice that the enquiry was saved locally instead.
