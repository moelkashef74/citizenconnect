# Generated by Django 5.0.2 on 2024-04-22 22:30

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports3', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report_cat_three',
            name='image',
            field=models.ImageField(storage=django.core.files.storage.FileSystemStorage(location='/home/citizenconnectt/citizenconnect/media'), upload_to='reports3/'),
        ),
    ]
