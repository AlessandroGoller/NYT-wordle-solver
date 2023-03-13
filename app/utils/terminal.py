import subprocess

from app.dependency import get_settings

settings = get_settings()

def open_chrome()->None:
    # Open Chrome
    path = f'{settings.CHROMEPATH}\chrome.exe' # noqa
    command = f'--remote-debugging-port={settings.PORT}'
    subprocess.Popen([path, command])
