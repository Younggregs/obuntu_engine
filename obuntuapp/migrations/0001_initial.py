# Generated by Django 3.1.1 on 2021-02-24 23:32

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SenatorialZone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=350)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Lga',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=350)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('senatorialzone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='obuntuapp.senatorialzone')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=350)),
                ('phone', models.CharField(max_length=19)),
                ('password', models.CharField(max_length=350)),
                ('email', models.EmailField(default='', max_length=254)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('lga', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='obuntuapp.lga')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
    ]
