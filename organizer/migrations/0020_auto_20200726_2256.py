# Generated by Django 3.0.5 on 2020-07-26 20:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizer', '0019_auto_20200707_0046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gogame',
            name='date',
            field=models.DateField(default=datetime.date(2020, 7, 26)),
        ),
    ]