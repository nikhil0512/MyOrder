# Generated by Django 3.0.6 on 2020-06-11 09:24

from django.db import migrations, models
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('adminpanel', '0007_auto_20200531_1927'),
    ]

    operations = [
        migrations.AddField(
            model_name='items',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='items',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
