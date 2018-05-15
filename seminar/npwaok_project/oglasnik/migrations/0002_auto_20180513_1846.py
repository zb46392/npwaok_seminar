# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-13 18:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('oglasnik', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subcategory',
            name='idCategory',
        ),
        migrations.RemoveField(
            model_name='ad',
            name='IdSubcategory',
        ),
        migrations.AddField(
            model_name='ad',
            name='Idcategory',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='oglasnik.Category'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Subcategory',
        ),
    ]
