# Generated by Django 3.1.1 on 2021-07-27 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminABC', '0007_account_internalid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='internalId',
            field=models.CharField(default=None, max_length=50),
        ),
    ]