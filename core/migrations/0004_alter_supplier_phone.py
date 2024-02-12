# Generated by Django 4.2 on 2024-01-26 09:47

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_supplier_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supplier',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(default='+2544567890', max_length=128, region=None, unique=True),
        ),
    ]