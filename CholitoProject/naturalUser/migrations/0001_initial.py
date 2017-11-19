# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-19 02:10
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import naturalUser.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ong', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NaturalUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(default=naturalUser.models.default_avatar, upload_to='n_users/avatar/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ONGLike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('natural_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='naturalUser.NaturalUser')),
                ('ong', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ong.ONG')),
            ],
        ),
    ]
