# Generated by Django 3.0.4 on 2020-05-19 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='slug',
            field=models.SlugField(default='-', unique=True),
            preserve_default=False,
        ),
    ]