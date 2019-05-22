# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-05-20 08:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meal', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FormId',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('forId', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'formID表',
                'db_table': 'form',
            },
        ),
    ]
