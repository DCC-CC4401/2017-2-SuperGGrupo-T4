from django.db import models


class AnimalType(models.Model):
    name = models.TextField(max_length=100)

    def __str__(self):
        return self.name


class Complaint(models.Model):
    COMPLAINT_OPTIONS = (
        (1, "Abandono en la calle"),
        (2, "Exposición a temperaturas extremas"),
        (3, "Falta de agua"),
        (4, "Falta de comida"),
        (5, "Violencia"),
        (6, "Venta ambulante"),
    )

    COMPLAINT_STATUS = (
        (1, "Enviado"),
        (2, "En Gestión"),
        (3, "Resuleta"),
        (4, "Erronea"),
    )

    GENDER_OPTIONS = (
        (1, "Macho"),
        (2, "Hembra"),
    )

    WOUND_OPTIONS = (
        (True, "Si"),
        (False, "No"),
    )

    description = models.TextField(max_length=1000)
    case = models.SmallIntegerField(choices=COMPLAINT_OPTIONS)
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    lng = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    directions = models.TextField(max_length=200, null=True)
    status = models.SmallIntegerField(choices=COMPLAINT_STATUS)
    animal_type = models.ForeignKey(AnimalType)
    gender = models.SmallIntegerField(choices=GENDER_OPTIONS)
    wounded = models.BooleanField(choices = WOUND_OPTIONS)
    color = models.TextField(max_length=50)

    def __str__(self):
        return "Complaint #" + str(self.pk)


class ComplaintImage(models.Model):
    image = models.ImageField(upload_to='complaints/')
    complaint = models.ForeignKey('Complaint', on_delete=models.CASCADE)
