# Generated by Django 4.2.3 on 2023-08-31 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='subscript',
            field=models.BooleanField(default=False),
        ),
    ]
