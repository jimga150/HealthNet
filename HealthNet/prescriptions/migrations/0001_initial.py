# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2017-04-20 03:15
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
            name='Prescription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_prescribed', models.DateTimeField()),
                ('drug', models.CharField(max_length=500)),
                ('dosage', models.DecimalField(decimal_places=3, max_digits=6)),
                ('Dose_units', models.CharField(choices=[('mg', 'milligrams'), ('ug', 'micrograms'), ('pg', 'picograms'), ('g', 'grams')], default='mg', max_length=10)),
                ('rate', models.PositiveSmallIntegerField()),
                ('Time_units', models.CharField(choices=[('/D', 'per Day'), ('/h', 'per Hour'), ('/W', 'per Week'), ('/M', 'per Month')], default='/D', max_length=9)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Doctor', verbose_name='Doctor')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Patient', verbose_name='Patient')),
            ],
        ),
    ]