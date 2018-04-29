# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-04-28 17:33
from __future__ import unicode_literals

import api.models
from django.db import migrations, models
import spacelaunchnow.storage_backends


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0024_auto_20180426_1901'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agency',
            name='ceo',
            field=models.CharField(blank=True, default=None, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='agency',
            name='logo_url',
            field=models.FileField(blank=True, default=None, null=True, storage=spacelaunchnow.storage_backends.LogoStorage(), upload_to=api.models.image_path),
        ),
    ]
