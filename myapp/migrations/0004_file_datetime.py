# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-08-03 15:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_auto_20180803_1244'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='datetime',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
