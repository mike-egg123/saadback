# Generated by Django 2.2 on 2020-12-05 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0003_auto_20201202_1712'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='blog',
        ),
        migrations.AddField(
            model_name='report',
            name='blog_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
