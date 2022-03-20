#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(os.path.join(ROOT_DIR, ".env"))


def main():
    """Run administrative tasks."""

    if os.environ.get("ENV"):
        # TODO : check if file exist
        env_file = "app.settings." + str(os.environ.get("ENV"))
    else:
        env_file = "app.settings.local"

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", env_file)
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
