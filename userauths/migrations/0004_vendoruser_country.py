# Generated by Django 4.2 on 2024-02-29 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("userauths", "0003_alter_user_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="vendoruser",
            name="country",
            field=models.CharField(default="Kenya", max_length=30),
        ),
    ]