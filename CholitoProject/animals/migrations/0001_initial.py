# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-17 19:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('complaint', '0001_initial'),
        ('naturalUser', '0001_initial'),
        ('ong', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Adopt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sent', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Animal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=100)),
                ('gender', models.SmallIntegerField(choices=[(1, 'Macho'), (2, 'Hembra')])),
                ('description', models.TextField(max_length=1000)),
                ('color', models.TextField(max_length=50)),
                ('estimated_age', models.PositiveSmallIntegerField()),
                ('days_in_adoption', models.IntegerField()),
                ('animal_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='complaint.AnimalType')),
                ('ong', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ong.ONG')),
            ],
        ),
        migrations.CreateModel(
            name='AnimalImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='animals/')),
                ('animal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='animals.Animal')),
            ],
        ),
        migrations.AddField(
            model_name='adopt',
            name='animal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='animals.Animal'),
        ),
        migrations.AddField(
            model_name='adopt',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='naturalUser.NaturalUser'),
        ),
    ]
