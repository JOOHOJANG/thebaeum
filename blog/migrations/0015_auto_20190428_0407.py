# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-04-27 19:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_auto_20190428_0400'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='tutor_num',
            field=models.CharField(max_length=200),
        ),
    ]
