# Generated by Django 3.0.6 on 2020-05-30 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0005_items_sub_items'),
    ]

    operations = [
        migrations.AlterField(
            model_name='items',
            name='sub_items',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]