# Generated by Django 5.0.2 on 2024-04-03 13:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0003_alter_problem_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='problem',
            name='category',
        ),
    ]
