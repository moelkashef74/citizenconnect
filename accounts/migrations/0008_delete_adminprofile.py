# Generated by Django 5.0.2 on 2024-05-05 01:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_adminprofile_delete_admin'),
    ]

    operations = [
        migrations.DeleteModel(
            name='AdminProfile',
        ),
    ]