BarberPro Booking System

A modern barber shop booking system built with Django and PostgreSQL.

Features
Multi-barber booking system
Appointment calendar
Dashboard statistics
Admin authentication system
Appointment management
PDF export
Responsive design
PostgreSQL database support
Mobile-friendly UI
Technologies Used
Python 3.11
Django 5
PostgreSQL
HTML5
CSS3
JavaScript
Gunicorn
WhiteNoise
Screenshots
Booking Page
Customer booking form
Barber selection
Service selection
Date & time booking
Calendar
Monthly appointment view
Appointments per barber
Service & pricing display
Dashboard
Statistics
Charts
Barber analytics
Service analytics
Installation
Clone Repository
git clone https://github.com/DoumanisKostas/barberpro-booking-system.git
cd barberpro-booking-system
Create Virtual Environment
python -m venv venv

Activate virtual environment:

Windows
venv\Scripts\activate
Linux / Mac
source venv/bin/activate
Install Requirements
pip install -r requirements.txt
PostgreSQL Setup

Create a PostgreSQL database:

barberpro_db

Update settings.py:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'barberpro_db',
        'USER': 'postgres',
        'PASSWORD': 'YOUR_PASSWORD',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
Run Migrations
python manage.py migrate
Create Admin User
python manage.py createsuperuser
Run Server
python manage.py runserver

Open:

http://127.0.0.1:8000
Deploy

This project supports deployment with:

Render
Railway

Production stack:

Gunicorn
WhiteNoise
PostgreSQL
Future Improvements
Email notifications
SMS notifications
WhatsApp integration
Online payments
Customer accounts
Advanced analytics
Author

Konstantinos Doumanis

GitHub:
DoumanisKostas GitHub
