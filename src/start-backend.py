import os
import subprocess


def start() -> None:  # For windows
    os.system('cmd /c "python backend/manage.py runserver')


if __name__ == '__main__':
    start()
