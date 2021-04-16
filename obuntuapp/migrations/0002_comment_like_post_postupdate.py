# Generated by Django 3.1.1 on 2021-04-09 09:48

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('obuntuapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('title', models.TextField()),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('account', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='obuntuapp.account')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='PostUpdate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('post', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='obuntuapp.post')),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('account', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='obuntuapp.account')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('account', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='obuntuapp.account')),
                ('post', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='obuntuapp.post')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
    ]