import unittest
from unittest.mock import patch

from app.models.prediction import Prediction
from app.services.dashboard_service import get_album_slug_for_prediction
from app.services.email_service import send_welcome_email


class DashboardAndEmailTests(unittest.TestCase):
    def test_processed_dashboard_images_fall_back_to_glass_facades(self):
        prediction = Prediction(
            id=1,
            user_id=1,
            original_image_path="uploads/original/upload_123.jpg",
            output_image_path="uploads/output/result_123.png",
            status="completed",
            original_filename="IMG_1234.jpg",
            stored_filename="upload_123.jpg",
            source="dashboard",
        )

        self.assertEqual(get_album_slug_for_prediction(prediction), "glass-facades")

    def test_gmail_sender_uses_default_host_when_mail_host_is_missing(self):
        smtp_instance = None

        class FakeSMTP:
            def __init__(self, host, port, timeout=0):
                nonlocal smtp_instance
                smtp_instance = self
                self.host = host
                self.port = port
                self.timeout = timeout
                self.login_args = None
                self.sent = False

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc, tb):
                return False

            def ehlo(self):
                return None

            def starttls(self):
                return None

            def login(self, username, password):
                self.login_args = (username, password)

            def sendmail(self, from_email, recipients, message):
                self.sent = True

        with (
            patch("app.services.email_service.settings.SMTP_HOST", ""),
            patch("app.services.email_service.settings.SMTP_PORT", 587),
            patch("app.services.email_service.settings.SMTP_USER", "glassclear090@gmail.com"),
            patch("app.services.email_service.settings.SMTP_APP_PASSWORD", "app-password"),
            patch("app.services.email_service.settings.SMTP_FROM_EMAIL", "glassclear090@gmail.com"),
            patch("smtplib.SMTP", FakeSMTP),
        ):
            send_welcome_email("misbah@example.com", "Misbah")

        self.assertIsNotNone(smtp_instance)
        self.assertEqual(smtp_instance.host, "smtp.gmail.com")
        self.assertEqual(smtp_instance.login_args, ("glassclear090@gmail.com", "app-password"))
        self.assertTrue(smtp_instance.sent)


if __name__ == "__main__":
    unittest.main()
