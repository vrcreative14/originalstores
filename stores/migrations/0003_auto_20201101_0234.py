# Generated by Django 3.0.8 on 2020-10-31 21:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0002_auto_20201101_0151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='store_details',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, to='stores.StoreDetails'),
        ),
    ]
