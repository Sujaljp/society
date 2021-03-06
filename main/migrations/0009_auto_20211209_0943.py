# Generated by Django 3.2.10 on 2021-12-09 04:13

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0008_service_service_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='service_details',
            field=models.TextField(blank=True),
        ),
        migrations.CreateModel(
            name='Bills',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('repairs_maintenance_charges', models.IntegerField()),
                ('society_service_charges', models.IntegerField()),
                ('sinking_fund_charges', models.IntegerField()),
                ('parking_charges', models.IntegerField()),
                ('charity_charges', models.IntegerField()),
                ('publish_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('due_date', models.DateTimeField()),
                ('flat_no_and_date', models.CharField(max_length=100)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
