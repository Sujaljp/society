# Generated by Django 3.2.9 on 2021-11-27 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('header_notice', models.CharField(max_length=100)),
                ('details_notice', models.TextField()),
            ],
        ),
    ]
