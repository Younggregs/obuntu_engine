# Generated by Django 3.1.1 on 2021-04-29 22:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('obuntuapp', '0013_chat'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chat',
            options={'ordering': ['date']},
        ),
        migrations.AlterField(
            model_name='account',
            name='about',
            field=models.CharField(default='Obuntu: I am because you are.', max_length=150),
        ),
    ]
