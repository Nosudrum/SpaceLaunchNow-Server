# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-11-28 22:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_auto_20181127_2322'),
    ]

    operations = [
        migrations.AddField(
            model_name='astronauts',
            name='slug',
            field=models.SlugField(max_length=100, null=True, unique=True),
        ),
    ]
