# Generated by Django 4.2.6 on 2023-10-13 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='time_completed',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]