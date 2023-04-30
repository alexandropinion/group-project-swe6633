import os
import subprocess


def start() -> None:  # For windows
    os.system('cmd /c "python ./manage.py runserver')
    # os.system('cmd /c cd frontend')
    # os.system('cmd /c cd npm start')


#: Start application
if __name__ == '__main__':
    start()
