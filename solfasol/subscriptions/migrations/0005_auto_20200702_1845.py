# Generated by Django 3.0.7 on 2020-07-02 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0004_subscription_renewal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='renewal',
            field=models.BooleanField(choices=[(False, 'New subscription'), (True, 'Renewal')], default=False, verbose_name='subscription status'),
        ),
    ]
