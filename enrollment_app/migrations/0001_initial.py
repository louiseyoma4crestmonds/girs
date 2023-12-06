# Generated by Django 3.2.9 on 2023-11-28 22:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EnrollmentAnswers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('firstName', models.CharField(blank=True, max_length=20)),
                ('middleName', models.CharField(blank=True, max_length=20)),
                ('surname', models.CharField(blank=True, max_length=20)),
                ('countryCode', models.CharField(blank=True, max_length=5)),
                ('phoneNumber', models.CharField(blank=True, max_length=15)),
            ],
        ),
    ]