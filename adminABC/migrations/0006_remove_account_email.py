# Generated by Django 3.1.1 on 2021-07-25 08:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminABC', '0005_account_ward'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='email',
        ),
    ]
