# Generated by Django 3.2.9 on 2023-12-05 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TouristSites',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place', models.CharField(default='Tourist Site', max_length=255)),
                ('longitude', models.CharField(default='0', max_length=255)),
                ('latitude', models.CharField(default='0', max_length=255)),
            ],
        ),
    ]