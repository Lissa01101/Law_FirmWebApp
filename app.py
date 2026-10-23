from flask import Flask, render_template, request, flash, redirect, url_for
from pathlib import Path
from datetime import datetime
from email.message import EmailMessage
import urllib.parse
import json
import os
import smtplib

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-only-change-this-secret-key")

MESSAGES_FILE = Path(__file__).with_name("enquiries.json")

# International format without symbols (+, -, spaces) or leading zeros
# If your South African number is 074 827 4502, it should be 27748274502
WHATSAPP_NUMBER = os.environ.get("WHATSAPP_NUMBER", "27748274502") 


def send_enquiry_email(enquiry):
    """Send an enquiry using SMTP environment settings. Returns (sent, reason)."""
    host = os.environ.get("SMTP_HOST")
    port = int(os.environ.get("SMTP_PORT", "587"))
    username = os.environ.get("SMTP_USERNAME")
    password = os.environ.get("SMTP_PASSWORD")
    recipient = os.environ.get("ENQUIRY_TO_EMAIL")
    sender = os.environ.get("ENQUIRY_FROM_EMAIL", username or "")

    missing = [key for key, value in {
        "SMTP_HOST": host,
        "SMTP_USERNAME": username,
        "SMTP_PASSWORD": password,
        "ENQUIRY_TO_EMAIL": recipient,
        "ENQUIRY_FROM_EMAIL or SMTP_USERNAME": sender,
    }.items() if not value]

    if missing:
        return False, "Email is not configured yet. Your enquiry was saved locally."

    msg = EmailMessage()
    msg["Subject"] = f"Website enquiry: {enquiry['service'] or 'General enquiry'}"
    msg["From"] = sender
    msg["To"] = recipient
    msg["Reply-To"] = enquiry["email"]
    msg.set_content(
        "A new enquiry was submitted through the law firm website.\n\n"
        f"Name: {enquiry['name']}\n"
        f"Email: {enquiry['email']}\n"
        f"Phone: {enquiry['phone'] or 'Not provided'}\n"
        f"Service: {enquiry['service'] or 'Not specified'}\n\n"
        f"Message:\n{enquiry['message']}\n\n"
        f"Submitted at: {enquiry['submitted_at']}\n"
    )

    try:
        with smtplib.SMTP(host, port, timeout=15) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(username, password)
            server.send_message(msg)
        return True, "Enquiry email sent."
    except (smtplib.SMTPException, OSError) as exc:
        app.logger.exception("Unable to send enquiry email")
        return False, "Email could not be sent right now. Your enquiry was saved locally."


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        service = request.form.get("service", "").strip()
        message = request.form.get("message", "").strip()

        if not name or not email or not message:
            flash("Please complete your name, email address and message.", "error")
            return redirect(url_for("home") + "#contact")

        if len(name) > 120 or len(email) > 254 or len(phone) > 50 or len(service) > 120 or len(message) > 5000:
            flash("One or more fields are too long. Please shorten your enquiry and try again.", "error")
            return redirect(url_for("home") + "#contact")

        enquiry = {
            "name": name,
            "email": email,
            "phone": phone,
            "service": service,
            "message": message,
            "submitted_at": datetime.now().isoformat(timespec="seconds"),
        }

        existing = []
        if MESSAGES_FILE.exists():
            try:
                existing = json.loads(MESSAGES_FILE.read_text(encoding="utf-8"))
                if not isinstance(existing, list):
                    existing = []
            except (json.JSONDecodeError, OSError):
                existing = []

        existing.append(enquiry)
        try:
            MESSAGES_FILE.write_text(
                json.dumps(existing, indent=2, ensure_ascii=False),
                encoding="utf-8"
            )
        except OSError:
            app.logger.exception("Unable to save enquiry locally")

        sent, reason = send_enquiry_email(enquiry)
        if sent:
            flash("Thank you. Your enquiry has been sent to the firm.", "success")
        else:
            flash(reason, "error")
        return redirect(url_for("home") + "#contact")

    # FIX: Added back the missing template return statement for standard GET requests
    return render_template("index.html")


@app.route('/whatsapp-redirect')
def whatsapp_redirect():
    message = "Hello, I would like to make a legal enquiry."
    encoded_message = urllib.parse.quote(message)
    
    whatsapp_url = f"https://wa.me/{WHATSAPP_NUMBER}?text={encoded_message}"
    return redirect(whatsapp_url)



if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG", "0") == "1")
