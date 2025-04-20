"""Email sending using Resend service"""
import os
import resend
from flask import current_app

resend.api_key = os.environ.get("RESEND_API_KEY")

def send_email(recipient, subject, body):
    """Send email using Resend service"""
    try:
        params = {
            "from": os.environ.get("RESEND_FROM_EMAIL", "noreply@yourdomain.com"),
            "to": [recipient],
            "subject": subject,
            "html": body,
        }
        response = resend.Emails.send(params)
        current_app.logger.info(f"Email sent to {recipient}")
        return response
    except Exception as e:
        current_app.logger.error(f"Failed to send email: {str(e)}")
        raise

