# Generated by Django 3.0.4 on 2020-03-30 16:52

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0020_auto_20200315_1701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='added',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]