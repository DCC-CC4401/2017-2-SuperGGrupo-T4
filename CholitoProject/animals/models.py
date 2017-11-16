from django.db import models

from complaint.models import Complaint, AnimalType
from naturalUser.models import NaturalUser
from ong.models import ONG


class AnimalImage(models.Model):
    image = models.ImageField(upload_to='animals/')
    animal = models.ForeignKey('Animal', on_delete=models.CASCADE)


class Animal(models.Model):
    GENDER_OPTIONS = (
        (1, "Macho"),
        (2, "Hembra"),
    )

    name = models.TextField(max_length=100)
    gender = models.SmallIntegerField(choices=GENDER_OPTIONS)
    description = models.TextField(max_length=1000)
    animal_type = models.ForeignKey(AnimalType)
    color = models.TextField(max_length=50)
    estimated_age = models.PositiveSmallIntegerField()
    admission_date = models.DateTimeField(auto_now_add = True)
    # TODO: delete when ong is deleted?
    ong = models.ForeignKey(ONG)

    def __str__(self):
        return self.name + " - " + self.animal_type.name


class Adopt(models.Model):
    user = models.ForeignKey(NaturalUser)
    animal = models.ForeignKey(Animal)
    sent = models.DateTimeField(auto_now_add=True)
