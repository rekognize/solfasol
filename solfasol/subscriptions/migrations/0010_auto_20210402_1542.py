# Generated by Django 3.1.2 on 2021-04-02 12:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0009_auto_20210402_1409'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subscription',
            old_name='sub_type',
            new_name='type',
        ),
    ]
