# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-02-02 19:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0066_auto_20190131_2129'),
    ]

    operations = [
        migrations.RenameField(
            model_name='spacecraftflight',
            old_name='splashdown',
            new_name='mission_end',
        ),
    ]
