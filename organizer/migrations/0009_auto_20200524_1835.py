# Generated by Django 3.0.5 on 2020-05-24 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizer', '0008_auto_20200524_1605'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip',
            name='duration',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='trip',
            name='transport',
            field=models.CharField(default='car', max_length=50),
        ),
    ]
