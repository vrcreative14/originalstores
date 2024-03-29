# Generated by Django 3.1.2 on 2020-11-12 12:49

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20201111_2126'),
    ]

    operations = [
        migrations.CreateModel(
            name='PhoneOTP',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(blank=True, max_length=13, null=True, unique=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+99999999", regex='^\\+?1?\\d{9,14}$')])),
                ('otp', models.CharField(blank=True, max_length=9, null=True)),
                ('count', models.IntegerField(default=0, help_text='Number of otp sent')),
            ],
        ),
    ]
