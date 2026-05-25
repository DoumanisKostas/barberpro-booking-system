import subprocess
import webbrowser
import time

server = subprocess.Popen(
    ["python", "manage.py", "runserver"]
)

time.sleep(8)

webbrowser.open("http://127.0.0.1:8000")

server.wait()