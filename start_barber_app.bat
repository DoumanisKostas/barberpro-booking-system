@echo off
cd /d C:\Projects\barber_booking_app

start "" cmd /k "C:\Projects\barber_booking_app\venv\Scripts\python.exe manage.py runserver"

timeout /t 3

start http://127.0.0.1:8000

pause