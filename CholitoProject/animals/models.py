from django.db import models
from django.utils import timezone

from complaint.models import Complaint, AnimalType
from naturalUser.models import NaturalUser
from ong.models import ONG


def default_avatar():
    return 'animals/animal-default.jpg'


class AnimalImage(models.Model):
    image = models.ImageField(upload_to='animals/')
    animal = models.ForeignKey('Animal', on_delete=models.CASCADE)


class Animal(models.Model):
    GENDER_OPTIONS = (
        (1, "Macho"),
        (2, "Hembra"),
    )

    ADOPTION_OPTIONS = (
        (1, "En adopción"),
        (2, "Procesando Solicitud Adopción"),
        (3, "Adoptado"),
    )

    STERILIZED_OPTIONS = (
        (True, "Sí"),
        (False, "No")
    )

    name = models.TextField(max_length=100)
    gender = models.SmallIntegerField(choices=GENDER_OPTIONS, default=1)
    description = models.TextField(max_length=1000)
    animal_type = models.ForeignKey(AnimalType)
    color = models.TextField(max_length=50)
    estimated_age = models.PositiveSmallIntegerField()
    admission_date = models.DateField(default=timezone.now)
    adoption_state = models.SmallIntegerField(choices=ADOPTION_OPTIONS,
                                              default=1)
    is_sterilized = models.BooleanField(choices=STERILIZED_OPTIONS,
                                        default=False)
    sterilized_date = models.DateField(null=True)
    adoption_date = models.DateField(null=True)
    ong = models.ForeignKey(ONG, on_delete=models.CASCADE)
    avatar = models.ImageField(default=default_avatar, upload_to="animals/", blank=True)

    def __str__(self):
        return self.name + " - " + self.animal_type.name


class Adopt(models.Model):
    user = models.ForeignKey(NaturalUser)
    animal = models.ForeignKey(Animal)
    sent = models.DateTimeField(auto_now_add=True)
