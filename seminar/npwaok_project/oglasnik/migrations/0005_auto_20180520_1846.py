# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-20 18:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('oglasnik', '0004_customuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ad',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='oglasnik.CustomUser'),
        ),
    ]