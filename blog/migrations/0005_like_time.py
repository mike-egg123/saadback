# Generated by Django 2.2 on 2020-12-02 17:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20201125_2257'),
    ]

    operations = [
        migrations.AddField(
            model_name='like',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 2, 17, 12, 4, 829732)),
        ),
    ]
