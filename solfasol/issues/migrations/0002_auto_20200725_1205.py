# Generated by Django 3.0.7 on 2020-07-25 09:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='page',
            options={'ordering': ('number',), 'verbose_name': 'page', 'verbose_name_plural': 'pages'},
        ),
    ]
