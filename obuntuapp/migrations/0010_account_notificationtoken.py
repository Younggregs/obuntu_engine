# Generated by Django 3.1.1 on 2021-04-11 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('obuntuapp', '0009_account_isverified'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='notificationToken',
            field=models.CharField(default=None, max_length=1000),
        ),
    ]
