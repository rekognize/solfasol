# Generated by Django 3.1.1 on 2020-10-06 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publications', '0008_auto_20201006_2245'),
    ]

    operations = [
        migrations.AddField(
            model_name='publication',
            name='slug',
            field=models.SlugField(default='-'),
            preserve_default=False,
        ),
    ]
