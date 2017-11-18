from django.contrib.auth.models import User, Permission
from django.db import models
from django.shortcuts import render

from ong.models import ONG


def default_avatar():
    return 'n_users/avatar/user-default.jpg'


class NaturalUser(models.Model):
    user = models.OneToOneField(User)
    avatar = models.ImageField(upload_to='n_users/avatar/', default=default_avatar)

    def save(self, *args, **kwargs):
        super(NaturalUser, self).save(*args, **kwargs)
        if not self.user.has_perm('natural_user_access'):
            permission = Permission.objects.get(codename='natural_user_access')
            self.user.user_permissions.add(permission)
        self.user.save()

    def __str__(self):
        return "Natural user " + self.user.username

    def get_index(self, request, context=None):
        liked, not_liked = self.filter_ongs(context['ongs'])
        context['liked_ongs'] = liked
        context['ongs'] = not_liked
        return render(request, 'index.html', context=context)

    def filter_ongs(self, ongs):
        liked_ongs = []
        not_liked_ongs = []
        for ong in ongs:
            print(ong.lat)
            if self.like_ong(ong):
                liked_ongs.append(ong)
            else :
                not_liked_ongs.append(ong)
        return (liked_ongs, not_liked_ongs)

    def like_ong(self, ong):
        return ONGLike.objects.all().filter(natural_user=self,ong=ong).count()



class ONGLike(models.Model):
    natural_user = models.ForeignKey(NaturalUser)
    ong = models.ForeignKey(ONG)
