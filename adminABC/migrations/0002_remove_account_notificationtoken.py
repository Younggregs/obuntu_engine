# Generated by Django 3.1.1 on 2021-07-20 00:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminABC', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='notificationToken',
        ),
    ]
