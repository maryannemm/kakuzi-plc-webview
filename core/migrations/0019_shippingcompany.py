# Generated by Django 4.2 on 2024-02-16 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_address_country_address_county'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShippingCompany',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(choices=[('fedex', 'FedEx'), ('dhl', 'DHL Express'), ('speedaf', 'SpeedAF')], default='speedaf', max_length=50)),
            ],
        ),
    ]