# Generated by Django 3.0.6 on 2020-06-18 14:21

import adminpanel.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0009_auto_20200615_2223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='items',
            name='image_url',
            field=models.ImageField(default='', upload_to=adminpanel.models.get_grocery_images),
        ),
    ]
