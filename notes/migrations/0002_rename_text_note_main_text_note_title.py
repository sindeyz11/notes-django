# Generated by Django 4.2.6 on 2023-10-15 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='note',
            old_name='text',
            new_name='main_text',
        ),
        migrations.AddField(
            model_name='note',
            name='title',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
