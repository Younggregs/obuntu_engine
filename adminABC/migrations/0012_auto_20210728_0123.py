# Generated by Django 3.1.1 on 2021-07-28 01:23

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('adminABC', '0011_auto_20210728_0119'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('internalId', models.CharField(default=None, max_length=50)),
                ('image', models.FileField(default=None, upload_to='')),
                ('password', models.CharField(max_length=350)),
                ('firstname', models.CharField(default='', max_length=350)),
                ('middlename', models.CharField(default='', max_length=350)),
                ('lastname', models.CharField(default='', max_length=350)),
                ('phone', models.CharField(default='', max_length=19)),
                ('gender', models.CharField(default='', max_length=19)),
                ('votercard', models.CharField(default='', max_length=150)),
                ('age', models.CharField(default='', max_length=150)),
                ('registrationNumber', models.CharField(max_length=50)),
                ('isOldMember', models.BooleanField(default=False)),
                ('isAdmin', models.BooleanField(default=False)),
                ('isSuperUser', models.BooleanField(default=False)),
                ('isVerified', models.BooleanField(default=False)),
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
                ('code', models.CharField(default='', max_length=3)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
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
            name='Ward',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=350)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('lga', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminABC.lga')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='SuperUserAdmin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('admin', models.IntegerField()),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('superUser', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='adminABC.account')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='PollingUnit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=350)),
                ('delimitation', models.CharField(max_length=50)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('ward', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminABC.ward')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.AddField(
            model_name='lga',
            name='senatorialzone',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminABC.senatorialzone'),
        ),
        migrations.CreateModel(
            name='AdminUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.IntegerField()),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('admin', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='adminABC.account')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.AddField(
            model_name='account',
            name='lga',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='adminABC.lga'),
        ),
        migrations.AddField(
            model_name='account',
            name='pollingUnit',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='adminABC.pollingunit'),
        ),
        migrations.AddField(
            model_name='account',
            name='ward',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='adminABC.ward'),
        ),
    ]