# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-11-03 21:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wedding', '0016_email_not_required'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='main_email',
            field=models.EmailField(default='no@no.com', max_length=254),
            preserve_default=False,
        ),
    ]
