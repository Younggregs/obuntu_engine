# Generated by Django 3.1.1 on 2021-04-10 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('obuntuapp', '0006_follow'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='image',
            field=models.FileField(default=None, upload_to=''),
        ),
    ]
