# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-04-27 12:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_auto_20190427_2136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='tutor_num',
            field=models.DecimalField(decimal_places=0, max_digits=8),
        ),
    ]