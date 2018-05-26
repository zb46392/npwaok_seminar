# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-26 10:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import oglasnik.models


class Migration(migrations.Migration):

    dependencies = [
        ('oglasnik', '0005_auto_20180520_1846'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdsImages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=oglasnik.models.advertisersDirectoryPath)),
                ('ad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='oglasnik.Ad')),
            ],
        ),
    ]