# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-04-27 10:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_request_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.CharField(choices=[('M/L', 'Major/Lan'), ('W/D', 'Work/Dev'), ('H', 'Hob')], default='', max_length=200),
        ),
    ]
