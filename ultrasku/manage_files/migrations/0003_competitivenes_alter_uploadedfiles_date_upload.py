# Generated by Django 4.2.3 on 2023-08-20 22:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manage_files', '0002_alter_uploadedfiles_date_upload'),
    ]

    operations = [
        migrations.CreateModel(
            name='Competitivenes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('partner_sku', models.CharField(blank=True, max_length=100, null=True)),
                ('sku_config', models.CharField(blank=True, max_length=100, null=True)),
                ('sku', models.CharField(blank=True, max_length=100, null=True)),
                ('family', models.CharField(blank=True, max_length=100, null=True)),
                ('product_type', models.CharField(blank=True, max_length=100, null=True)),
                ('brand', models.CharField(blank=True, max_length=100, null=True)),
                ('product_title', models.TextField(blank=True, null=True)),
                ('country_code', models.CharField(blank=True, max_length=100, null=True)),
                ('recommended_action', models.CharField(blank=True, max_length=100, null=True)),
                ('live_mp', models.CharField(blank=True, max_length=100, null=True)),
                ('current_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('platform_recommended_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('current_fbn_stock', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('current_b2b_stock', models.BooleanField()),
                ('days_of_coverage', models.CharField(blank=True, max_length=100, null=True)),
                ('b2b_processing_days', models.CharField(blank=True, max_length=100, null=True)),
                ('lowest_processing_days', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('lowest_mp_fbn_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('lowest_mp_b2b_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('external_competition_price', models.CharField(blank=True, max_length=100, null=True)),
                ('average_sku_selling_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('your_visitors_15_days', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('revenue_shipped_15_days', models.BooleanField()),
                ('shipped_units_15_days', models.BooleanField()),
            ],
        ),
        migrations.AlterField(
            model_name='uploadedfiles',
            name='date_upload',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 8, 21, 1, 11, 37, 983613), null=True),
        ),
    ]
