# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2019-05-22 06:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meal', '0004_auto_20190521_1459'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dishestype',
            options={'verbose_name_plural': '菜单信息'},
        ),
        migrations.AlterField(
            model_name='disheslist',
            name='create',
            field=models.DateField(auto_now_add=True),
        ),
    ]
