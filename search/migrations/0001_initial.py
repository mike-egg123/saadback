# Generated by Django 2.2 on 2020-12-05 11:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Update_Log',
            fields=[
                ('ulid', models.AutoField(primary_key=True, serialize=False)),
                ('filename', models.CharField(max_length=50)),
                ('startlinenum', models.PositiveIntegerField()),
                ('finishlinenum', models.PositiveIntegerField()),
                ('updatetime', models.DateTimeField(auto_now_add=True)),
                ('updateadministrator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
