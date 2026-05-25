from django.db import models


class Barber(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Appointment(models.Model):
    customer_name = models.CharField("Ονοματεπώνυμο", max_length=100)
    phone = models.CharField("Τηλέφωνο", max_length=20)
    service = models.CharField("Υπηρεσία", max_length=100)
    date = models.DateField("Ημερομηνία")
    time = models.CharField("Ώρα", max_length=20)
    created_at = models.DateTimeField("Ημερομηνία καταχώρησης", auto_now_add=True)
    barber = models.ForeignKey(Barber,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return f"{self.customer_name} - {self.service}"