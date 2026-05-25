from django import forms
from .models import Appointment, Barber
from datetime import date

SERVICE_CHOICES = [
    ('Ανδρικό κούρεμα — 14€', 'Ανδρικό κούρεμα — 14€'),
    ('Μούσι — 7€', 'Μούσι — 7€'),
    ('Κούρεμα + μούσι — 16€', 'Κούρεμα + μούσι — 16€'),
    ('Ανδρικό κούρεμα + Λούσιμο — 17€', 'Ανδρικό κούρεμα + Λούσιμο — 17€'),
]


TIME_CHOICES = [
    ('09:00 π.μ.', '09:00 π.μ.'),
    ('09:30 π.μ.', '09:30 π.μ.'),
    ('10:00 π.μ.', '10:00 π.μ.'),
    ('10:30 π.μ.', '10:30 π.μ.'),
    ('11:00 π.μ.', '11:00 π.μ.'),
    ('11:30 π.μ.', '11:30 π.μ.'),
    ('12:00 μ.μ.', '12:00 μ.μ.'),
    ('12:30 μ.μ.', '12:30 μ.μ.'),
    ('01:00 μ.μ.', '01:00 μ.μ.'),
    ('01:30 μ.μ.', '01:30 μ.μ.'),
    ('02:00 μ.μ.', '02:00 μ.μ.'),
    ('02:30 μ.μ.', '02:30 μ.μ.'),
    ('03:00 μ.μ.', '03:00 μ.μ.'),
    ('03:30 μ.μ.', '03:30 μ.μ.'),
    ('04:00 μ.μ.', '04:00 μ.μ.'),
    ('04:30 μ.μ.', '04:30 μ.μ.'),
    ('05:00 μ.μ.', '05:00 μ.μ.'),
    ('05:30 μ.μ.', '05:30 μ.μ.'),
    ('06:00 μ.μ.', '06:00 μ.μ.'),
    ('06:30 μ.μ.', '06:30 μ.μ.'),
    ('07:00 μ.μ.', '07:00 μ.μ.'),
    ('07:30 μ.μ.', '07:30 μ.μ.'),
    ('08:00 μ.μ.', '08:00 μ.μ.'),
]


class AppointmentForm(forms.ModelForm):

    customer_name = forms.CharField(label='Ονοματεπώνυμο')
    phone = forms.CharField(label='Τηλέφωνο')

    service = forms.ChoiceField(
        choices=SERVICE_CHOICES,
        label='Υπηρεσία'
    )

    date = forms.DateField(
        label='Ημερομηνία',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    time = forms.ChoiceField(
        choices=TIME_CHOICES,
        label='Ώρα'
    )

    barber = forms.ModelChoiceField(
    queryset=Barber.objects.all(),
    label='Barber'
    )

    def __init__(self, *args, **kwargs):
        selected_date = kwargs.pop('selected_date', None)

        super().__init__(*args, **kwargs)

        self.booked_times = []

        if selected_date:
            self.fields['date'].initial = selected_date

            booked_times = Appointment.objects.filter(
                date=selected_date
            ).values_list('time', flat=True)

            booked_times = list(booked_times)

            updated_choices = []

            for time in TIME_CHOICES:
                if time[0] in booked_times:
                    updated_choices.append(
                        (
                            time[0],
                            f"{time[1]} ❌ Κρατημένο"
                        )
                    )
                else:
                    updated_choices.append(time)

            self.fields['time'].choices = updated_choices
            self.booked_times = booked_times

    def clean_date(self):
        selected_date = self.cleaned_data['date']

        # Παλιά ημερομηνία
        if selected_date < date.today():
            raise forms.ValidationError(
                "Δεν μπορείτε να κλείσετε ραντεβού σε παλιά ημερομηνία."
            )

        # Κυριακή
        if selected_date.weekday() == 6:
            raise forms.ValidationError(
                "Το κουρείο είναι κλειστό τις Κυριακές."
            )

        return selected_date

    def clean_time(self):
        selected_time = self.cleaned_data['time']
        selected_date = self.cleaned_data.get('date')

        if selected_date and Appointment.objects.filter(
            date=selected_date,
            time=selected_time
        ).exists():
            raise forms.ValidationError(
                "Η συγκεκριμένη ώρα είναι ήδη κρατημένη."
            )

        return selected_time

    class Meta:
        model = Appointment
        fields = ['date', 'customer_name', 'phone', 'barber', 'time', 'service']