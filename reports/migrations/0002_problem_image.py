# Generated by Django 5.0.2 on 2024-04-01 09:37

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='image',
            field=models.ImageField(null=True, storage=django.core.files.storage.FileSystemStorage(location='media'), upload_to='reports/'),
        ),
    ]
