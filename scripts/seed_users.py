"""Seed demo users for local development when the users table is empty (US03)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app import create_app
from app.services.auth_service import seed_demo_users


def main() -> None:
    app = create_app()
    with app.app_context():
        created = seed_demo_users()
        if created:
            print(f"Created {len(created)} demo user(s):")
            for user in created:
                print(f"  - {user.email} ({user.role})")
        else:
            print("Demo users already present.")
        print(
            "Demo passwords (local only): "
            "Admin123! / Dev123! / Viewer123! for admin@ / dev@ / viewer@taskflow.local"
        )


if __name__ == "__main__":
    main()
