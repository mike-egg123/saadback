# Generated by Django 2.2 on 2020-11-26 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='reportid',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
