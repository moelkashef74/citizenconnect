# Generated by Django 5.0.2 on 2024-05-03 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='category',
            field=models.CharField(default='cat1', max_length=20),
        ),
    ]
