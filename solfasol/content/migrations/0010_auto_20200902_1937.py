# Generated by Django 3.1.1 on 2020-09-02 16:37

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0009_content_publish_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='body',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='content',
            name='publish_at',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='Set a future date to publish later', verbose_name='publishing time'),
        ),
    ]
