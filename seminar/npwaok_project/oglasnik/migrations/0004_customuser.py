# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-19 11:12
from __future__ import unicode_literals

import django.contrib.auth.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
        ('oglasnik', '0003_auto_20180515_2045'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
