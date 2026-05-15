import unittest
from unittest.mock import patch

from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.api.routes.auth import register_user
from app.schemas.auth import RegisterRequest
from app.core.database import Base
from app.services.auth_service import authenticate_local_user, register_local_user
from app.services.email_service import send_welcome_email
from app.services.auth_validation import validate_email, validate_name, validate_password


class AuthValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine("sqlite:///:memory:")
        cls.SessionLocal = sessionmaker(bind=cls.engine, autocommit=False, autoflush=False)
        Base.metadata.create_all(bind=cls.engine)

    @classmethod
    def tearDownClass(cls):
        cls.engine.dispose()

    def setUp(self):
        self.db = self.SessionLocal()

    def tearDown(self):
        self.db.close()
        with self.engine.begin() as connection:
            for table in reversed(Base.metadata.sorted_tables):
                connection.execute(table.delete())

    def test_name_validation_rejects_symbols_and_short_values(self):
        with self.assertRaises(HTTPException) as short_name:
            validate_name("Mi")
        self.assertEqual(short_name.exception.detail, "Name must be at least 3 characters.")

        with self.assertRaises(HTTPException) as invalid_name:
            validate_name("Misbah123")
        self.assertEqual(invalid_name.exception.detail, "Name must contain only alphabets and spaces.")

    def test_email_and_password_validation(self):
        self.assertEqual(validate_email("  USER@Example.com "), "user@example.com")

        with self.assertRaises(HTTPException) as invalid_email:
            validate_email("wrong-email")
        self.assertEqual(invalid_email.exception.detail, "Enter a valid email address.")

        with self.assertRaises(HTTPException) as weak_password:
            validate_password("password")
        self.assertEqual(
            weak_password.exception.detail,
            "Password must include uppercase, lowercase, number, and special character.",
        )

    def test_register_user_normalizes_email_and_hashes_password(self):
        user = register_local_user(
            self.db,
            name="  Misbah   Khan  ",
            email="  MISBAH@EXAMPLE.COM ",
            password="Glass@123",
        )

        self.assertEqual(user.name, "Misbah Khan")
        self.assertEqual(user.email, "misbah@example.com")
        self.assertNotEqual(user.password_hash, "Glass@123")
        self.assertTrue(user.password_hash)

    def test_duplicate_email_is_rejected(self):
        register_local_user(
            self.db,
            name="Misbah Khan",
            email="misbah@example.com",
            password="Glass@123",
        )

        with self.assertRaises(HTTPException) as duplicate:
            register_local_user(
                self.db,
                name="Misbah Khan",
                email="MISBAH@example.com",
                password="Glass@123",
            )

        self.assertEqual(duplicate.exception.detail, "Email already registered.")

    def test_login_accepts_normalized_email_and_rejects_wrong_password(self):
        register_local_user(
            self.db,
            name="Misbah Khan",
            email="misbah@example.com",
            password="Glass@123",
        )

        user = authenticate_local_user(self.db, "  MISBAH@example.com ", "Glass@123")
        self.assertEqual(user.email, "misbah@example.com")

        with self.assertRaises(HTTPException) as invalid_password:
            authenticate_local_user(self.db, "misbah@example.com", "Wrong@123")

        self.assertEqual(invalid_password.exception.detail, "Invalid email or password.")

    def test_register_route_sends_welcome_email_after_signup(self):
        payload = RegisterRequest(
            name="Misbah Khan",
            email="misbah@example.com",
            password="Glass@123",
        )

        with patch("app.api.routes.auth.send_welcome_email") as mocked_email:
            user = register_user(payload, self.db)

        self.assertEqual(user.email, "misbah@example.com")
        mocked_email.assert_called_once_with("misbah@example.com", "Misbah Khan")

    def test_welcome_email_failure_does_not_raise(self):
        with patch("smtplib.SMTP", side_effect=RuntimeError("smtp down")):
            send_welcome_email("misbah@example.com", "Misbah Khan")


if __name__ == "__main__":
    unittest.main()
