# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-12-05 06:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_auto_20181205_0240'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='spacecraftconfiguration',
            options={'ordering': ['name'], 'verbose_name': 'Spacecraft Configuration', 'verbose_name_plural': 'Spacecraft Configurations'},
        ),
    ]
