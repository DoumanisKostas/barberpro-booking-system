from django.shortcuts import render, redirect, get_object_or_404 
from .forms import AppointmentForm
from .models import Appointment
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from datetime import datetime
import calendar

@login_required
def calendar_view(request):
    today = datetime.today()

    year = int(request.GET.get('year', today.year))
    month = int(request.GET.get('month', today.month))

    cal = calendar.Calendar(firstweekday=0)
    month_days = cal.monthdatescalendar(year, month)

    appointments = Appointment.objects.filter(
        date__year=year,
        date__month=month
    ).order_by('date', 'time')

    appointments_by_date = {}

    for appointment in appointments:
        appointments_by_date.setdefault(appointment.date, []).append(appointment)

    return render(
        request,
        'appointments/calendar.html',
        {
            'month_days': month_days,
            'appointments_by_date': appointments_by_date,
            'month': month,
            'year': year,
        }
    )


@login_required
def book_appointment(request):
    selected_date = request.GET.get('date') or request.POST.get('date')

    if request.method == 'POST':
        form = AppointmentForm(request.POST, selected_date=selected_date)

        if form.is_valid():
            appointment = form.save()

            subject = 'Νέα Κράτηση - BarberPro'

            message = f"""
Νέα κράτηση καταχωρήθηκε:

Όνομα: {appointment.customer_name}
Τηλέφωνο: {appointment.phone}
Υπηρεσία: {appointment.service}
Ημερομηνία: {appointment.date}
Ώρα: {appointment.time}
"""

            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.BARBER_EMAIL],
                fail_silently=False,
            )

            return redirect('booking_success')
    else:
        form = AppointmentForm(selected_date=selected_date)

    return render(request, 'appointments/book.html', {'form': form})
        
@login_required
def booking_success(request):
    return render(request, 'appointments/success.html')

@login_required
def appointment_list(request):
    search_query = request.GET.get('search')
    date_filter = request.GET.get('date')

    appointments = Appointment.objects.all().order_by('date', 'time')

    if search_query:
        appointments = appointments.filter(
            customer_name__icontains=search_query
        ) | appointments.filter(
            phone__icontains=search_query
        )

    if date_filter:
        appointments = appointments.filter(date=date_filter)

    return render(
        request,
        'appointments/appointment_list.html',
        {
            'appointments': appointments,
            'search_query': search_query,
            'date_filter': date_filter
        }
    )


@login_required
def delete_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.delete()
    return redirect('appointment_list')

@login_required
def edit_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    selected_date = request.GET.get('date') or request.POST.get('date') or appointment.date

    if request.method == 'POST':
        form = AppointmentForm(
            request.POST,
            instance=appointment,
            selected_date=selected_date
        )

        if form.is_valid():
            form.save()
            return redirect('appointment_list')
    else:
        form = AppointmentForm(
            instance=appointment,
            selected_date=selected_date
        )

    return render(
        request,
        'appointments/edit_appointment.html',
        {'form': form, 'appointment': appointment}
    )

@login_required
def dashboard(request):
    total_appointments = Appointment.objects.count()

    today_appointments = Appointment.objects.filter(
        date=datetime.today().date()
    ).count()

    barber_stats = Appointment.objects.values(
        'barber__name'
    ).annotate(
        total=Count('id')
    )

    service_stats = Appointment.objects.values(
        'service'
    ).annotate(
        total=Count('id')
    )

    max_barber_total = max([b['total'] for b in barber_stats], default=1)
    max_service_total = max([s['total'] for s in service_stats], default=1)

    return render(
        request,
        'appointments/dashboard.html',
        {
            'total_appointments': total_appointments,
            'today_appointments': today_appointments,
            'barber_stats': barber_stats,
            'service_stats': service_stats,
            'max_barber_total': max_barber_total,
            'max_service_total': max_service_total,
        }
    )


@login_required
def working_days(request):

    return render(
        request,
        'appointments/working_days.html'
    )



@login_required
def export_appointments_pdf(request):
    appointments = Appointment.objects.all().order_by('date', 'time')

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="appointments.pdf"'

    pdfmetrics.registerFont(
    TTFont('ArialGreek', 'C:/Windows/Fonts/arial.ttf')
)

    p = canvas.Canvas(response)
    p.setFont("ArialGreek", 14)

    p.drawString(100, 800, "Appointments List")

    y = 760
    counter = 1

    for appointment in appointments:
        p.setFont("ArialGreek", 10)

        p.drawString(50, y, f"{counter}. {appointment.customer_name}")
        y -= 20
        p.drawString(70, y, f"Phone: {appointment.phone}")
        y -= 20
        p.drawString(70, y, f"Service: {appointment.service}")
        y -= 20
        p.drawString(70, y, f"Date: {appointment.date}")
        y -= 20
        p.drawString(70, y, f"Time: {appointment.time}")
        y -= 30

        counter += 1

        if y < 80:
            p.showPage()
            y = 800

    p.save()
    return response

    