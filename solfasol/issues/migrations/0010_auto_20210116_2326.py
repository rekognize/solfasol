# Generated by Django 3.1.2 on 2021-01-16 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0009_auto_20200918_0020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='year',
            field=models.PositiveSmallIntegerField(choices=[(2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021)], verbose_name='year'),
        ),
    ]
