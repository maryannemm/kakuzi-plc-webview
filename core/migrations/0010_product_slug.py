# Generated by Django 4.2 on 2024-02-02 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_delete_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]
