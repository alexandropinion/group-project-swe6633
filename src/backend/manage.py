#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import logging
import os
from re import DEBUG
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


#: Main entry point of application
if __name__ == '__main__':
    logging.basicConfig(level=DEBUG)
    main()
