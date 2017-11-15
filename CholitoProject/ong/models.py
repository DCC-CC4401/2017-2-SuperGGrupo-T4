from django.contrib.auth.models import User, Permission
from django.db import models
from django.shortcuts import redirect


class ONG(models.Model):
    name = models.TextField(max_length=200)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lng = models.DecimalField(max_digits=9, decimal_places=6)
    # is this really needed?
    directions = models.TextField(max_length=200, null=True)
    avatar = models.ImageField(upload_to='ong/avatar/')

    def __str__(self):
        return self.name


class ONGUser(User):
    ong = models.ForeignKey('ONG')

    def __str__(self):
        return self.municipality.name + " User"

    def get_index(self, request, context):
        return redirect('/ong/')

    # TODO: add permission
    def save(self, *args, **kwargs):
        super(ONGUser, self).save(*args, **kwargs)
        if not self.user.has_perm('ong_user_access'):
            permission = Permission.objects.get(
                codename='ong_user_access')
            self.user.user_permissions.add(permission)
        self.user.save()
