from __future__ import annotations

from flask import Flask

from app.config import Config
from app.db import close_db, init_db


def create_app(config_object: type = Config) -> Flask:
    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static",
    )
    app.config.from_object(config_object)

    if not app.config.get("TESTING") and app.config.get("SECRET_KEY") in (
        None,
        "",
        "dev-only-secret-key",
    ):
        raise RuntimeError(
            "SECRET_KEY must be set via environment for non-testing runs "
            "(copy .env.example to .env and set a strong value)."
        )

    app.teardown_appcontext(close_db)

    from app.routes.auth import bp as auth_bp
    from app.routes.pages import bp as pages_bp
    from app.routes.tasks import bp as tasks_bp
    from app.routes.users import bp as users_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(pages_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(tasks_bp)

    with app.app_context():
        init_db()
        # Demo users for local and hosted demos (idempotent; US01/US03/US15).
        if not app.config.get("TESTING"):
            from app.services.auth_service import seed_demo_users

            seed_demo_users()

    return app
