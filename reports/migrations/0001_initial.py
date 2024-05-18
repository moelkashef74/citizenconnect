# Generated by Django 5.0.2 on 2024-05-18 14:58

import django.core.files.storage
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.CharField(editable=False, max_length=10, primary_key=True, serialize=False)),
                ('image', models.ImageField(storage=django.core.files.storage.FileSystemStorage(location='/home/citizenconnectt/citizenconnect/media'), upload_to='reports/')),
                ('description', models.TextField()),
                ('location', models.TextField()),
                ('status', models.CharField(default='reported', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('category', models.CharField(choices=[('Environmental', 'env'), ('Traffic', 'tr'), ('Electric', 'elec'), ('other', 'Other')], max_length=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reports', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
