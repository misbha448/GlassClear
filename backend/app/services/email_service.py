from __future__ import annotations

import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.core.config import settings

logger = logging.getLogger(__name__)


def _clean_setting(value: str | None) -> str:
    return str(value or "").strip()


def send_welcome_email(user_email: str, user_name: str) -> None:
    smtp_user = _clean_setting(settings.SMTP_USER)
    smtp_password = _clean_setting(settings.SMTP_APP_PASSWORD)
    smtp_from_email = _clean_setting(settings.SMTP_FROM_EMAIL) or smtp_user
    smtp_host = _clean_setting(settings.SMTP_HOST) or ("smtp.gmail.com" if smtp_user.lower().endswith("@gmail.com") else "")

    if not smtp_host or not smtp_from_email:
        logger.warning("Welcome email skipped because SMTP is not configured")
        return

    app_url = settings.FRONTEND_URL.rstrip("/")
    safe_name = user_name or "there"
    subject = "Welcome to GlassClear"
    text_body = (
        f"Hi {safe_name},\n\n"
        "Welcome to GlassClear!\n\n"
        "Your account has been created successfully. You can now upload architectural images, remove glare and "
        "reflections, manage processed results, create collections, and export client-ready outputs.\n\n"
        "Thank you for using GlassClear.\n\n"
        "Regards,\n"
        "GlassClear Team"
    )
    html_body = f"""
    <html>
      <body style="margin:0;padding:24px;background:#f5f7fb;font-family:Arial,sans-serif;color:#18253c;">
        <div style="max-width:640px;margin:0 auto;background:#ffffff;border-radius:18px;padding:32px;border:1px solid #d9e1ef;">
          <div style="font-size:13px;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;color:#5b6ee1;margin-bottom:12px;">GlassClear</div>
          <h1 style="margin:0 0 18px;font-size:28px;line-height:1.2;">Welcome to GlassClear</h1>
          <p style="margin:0 0 14px;font-size:15px;">Hi {safe_name},</p>
          <p style="margin:0 0 14px;font-size:15px;line-height:1.7;">
            Your account has been created successfully. You can now upload architectural images, remove glare and reflections,
            manage processed results, create collections, and export client-ready outputs.
          </p>
          <p style="margin:0 0 24px;font-size:15px;line-height:1.7;">
            Thank you for using GlassClear.
          </p>
          <a href="{app_url}" style="display:inline-block;padding:12px 18px;background:#1f6fff;color:#ffffff;text-decoration:none;border-radius:12px;font-weight:700;">
            Open GlassClear
          </a>
          <p style="margin:28px 0 0;font-size:14px;line-height:1.7;color:#4a5a77;">
            Regards,<br />GlassClear Team
          </p>
        </div>
      </body>
    </html>
    """

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = f"{settings.SMTP_FROM_NAME} <{smtp_from_email}>"
    message["To"] = user_email
    message.attach(MIMEText(text_body, "plain", "utf-8"))
    message.attach(MIMEText(html_body, "html", "utf-8"))

    try:
        with smtplib.SMTP(smtp_host, settings.SMTP_PORT, timeout=20) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            if smtp_user:
                server.login(smtp_user, smtp_password)
            server.sendmail(smtp_from_email, [user_email], message.as_string())
    except Exception:
        logger.exception("Failed to send welcome email to %s", user_email)
