# Generated by Django 3.1.2 on 2020-10-28 16:16

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20201028_2144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=13, null=True, unique=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+99999999", regex='^\\+?\\d(9,14)$')]),
        ),
    ]
