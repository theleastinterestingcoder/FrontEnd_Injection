# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-29 04:24
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('injection', '0002_auto_20170629_0406'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flagclaim',
            name='team_submit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
