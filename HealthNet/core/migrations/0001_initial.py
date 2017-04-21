# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2017-04-20 03:15
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phoneNum', models.CharField(max_length=11)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Hospital',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default='', max_length=100, verbose_name='Username')),
                ('time', models.DateTimeField(verbose_name='Date Logged')),
                ('type', models.CharField(max_length=100, verbose_name='Type')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
        migrations.CreateModel(
            name='Nurse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phoneNum', models.CharField(max_length=11)),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Hospital')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birthday', models.DateField(default='1800-01-01')),
                ('sex', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('N', 'Neither')], default='M', max_length=5)),
                ('blood_type', models.CharField(choices=[('A+', 'A+'), ('B+', 'B'), ('O+', 'O+'), ('AB+', 'AB+'), ('A-', 'A-'), ('B-', 'B-'), ('O-', 'O-'), ('AB-', 'AB-'), ('UN', 'Unknown')], default='UN', max_length=10)),
                ('height', models.CharField(max_length=7, null=True)),
                ('weight', models.PositiveSmallIntegerField(null=True)),
                ('allergies', models.TextField(default='', max_length=1000)),
                ('insurance_info', models.CharField(max_length=50)),
                ('emergency_contact', models.EmailField(max_length=254)),
                ('emergency_contact_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='emergency_user', to=settings.AUTH_USER_MODEL)),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='current_hospital', to='core.Hospital')),
                ('preferred_hospital', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='preferred_hospital', to='core.Hospital')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
