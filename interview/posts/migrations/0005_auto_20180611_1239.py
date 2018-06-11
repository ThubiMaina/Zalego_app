# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-11 09:39
from __future__ import unicode_literals

from django.db import migrations, models
import posts.models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_auto_20180611_1145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(height_field='height_field', null=True, upload_to=posts.models.upload_location, width_field='width_field'),
        ),
    ]