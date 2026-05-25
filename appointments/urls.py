from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_appointment, name='book_appointment'),
    path('success/', views.booking_success, name='booking_success'),
    path('appointments/', views.appointment_list, name='appointment_list'),
    path('delete/<int:appointment_id>/', views.delete_appointment, name='delete_appointment'),
    path('edit/<int:appointment_id>/', views.edit_appointment, name='edit_appointment'),
    path('working-days/', views.working_days, name='working_days'),
    path('export-pdf/', views.export_appointments_pdf, name='export_appointments_pdf'),
    path('calendar/', views.calendar_view, name='calendar_view'),
    path('dashboard/', views.dashboard, name='dashboard'),
]

path(
    'delete/<int:appointment_id>/',
    views.delete_appointment,
    name='delete_appointment'
),

