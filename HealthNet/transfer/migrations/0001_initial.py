# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2017-05-09 21:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transfer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('New_Hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Hospital')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Patient')),
            ],
        ),
    ]
