# Generated by Django 4.2.3 on 2023-08-31 16:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manage_files', '0004_delete_competitivenes_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadedfiles',
            name='date_upload',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 8, 31, 19, 44, 6, 243273), null=True),
        ),
    ]
