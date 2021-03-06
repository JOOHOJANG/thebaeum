# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-04-27 07:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('tutor_name', models.CharField(max_length=200)),
                ('tutor_num', models.DecimalField(decimal_places=12, max_digits=12)),
                ('tutor_career', models.TextField(max_length=10000)),
                ('class_info', models.TextField(max_length=10000)),
            ],
        ),
    ]
