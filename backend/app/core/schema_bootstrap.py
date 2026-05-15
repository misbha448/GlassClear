from sqlalchemy import inspect, text
from sqlalchemy.engine import Engine


PREDICTION_COLUMNS = {
    "project_id": "INTEGER",
    "original_filename": "VARCHAR",
    "stored_filename": "VARCHAR",
    "mime_type": "VARCHAR",
    "file_size": "INTEGER",
    "width": "INTEGER",
    "height": "INTEGER",
    "source": "VARCHAR DEFAULT 'dashboard'",
    "guest_image_token": "VARCHAR",
    "active_workspace": "BOOLEAN DEFAULT FALSE",
    "thumbnail_path": "VARCHAR",
    "category": "VARCHAR",
    "updated_at": "TIMESTAMP"
}

USER_COLUMNS = {
    "auth_provider": "VARCHAR DEFAULT 'local' NOT NULL",
    "google_id": "VARCHAR",
    "avatar_url": "VARCHAR",
    "is_email_verified": "BOOLEAN DEFAULT FALSE NOT NULL",
    "status": "VARCHAR DEFAULT 'active' NOT NULL",
}

BATCH_JOB_COLUMNS = {
    "zip_path": "VARCHAR",
}

SHARE_LINK_COLUMNS = {
    "is_active": "BOOLEAN DEFAULT TRUE NOT NULL",
}


def ensure_dashboard_schema(engine: Engine) -> None:
    inspector = inspect(engine)
    existing_tables = set(inspector.get_table_names())

    if "predictions" not in existing_tables:
        return

    with engine.begin() as connection:
        prediction_columns = {column["name"] for column in inspector.get_columns("predictions")}
        for column_name, column_type in PREDICTION_COLUMNS.items():
            if column_name not in prediction_columns:
                connection.execute(text(f"ALTER TABLE predictions ADD COLUMN {column_name} {column_type}"))

        if "users" in existing_tables:
            user_columns = {column["name"] for column in inspector.get_columns("users")}
            for column_name, column_type in USER_COLUMNS.items():
                if column_name not in user_columns:
                    connection.execute(text(f"ALTER TABLE users ADD COLUMN {column_name} {column_type}"))

        if "batch_jobs" in existing_tables:
            batch_job_columns = {column["name"] for column in inspector.get_columns("batch_jobs")}
            for column_name, column_type in BATCH_JOB_COLUMNS.items():
                if column_name not in batch_job_columns:
                    connection.execute(text(f"ALTER TABLE batch_jobs ADD COLUMN {column_name} {column_type}"))

        if "share_links" in existing_tables:
            share_link_columns = {column["name"] for column in inspector.get_columns("share_links")}
            for column_name, column_type in SHARE_LINK_COLUMNS.items():
                if column_name not in share_link_columns:
                    connection.execute(text(f"ALTER TABLE share_links ADD COLUMN {column_name} {column_type}"))
