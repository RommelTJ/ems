# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-16 18:02
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import feedback.models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0003_auto_20170316_1800'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='email',
            field=models.CharField(max_length=150, validators=[django.core.validators.EmailValidator(whitelist=[b'ems']), django.core.validators.MinLengthValidator(7), django.core.validators.MaxLengthValidator(100, message=b'Seriously? This is too long.'), feedback.models.validate_allowed_domains]),
        ),
    ]
