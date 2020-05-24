# Generated by Django 3.0.4 on 2020-05-24 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0017_remove_content_body'),
    ]

    operations = [
        migrations.AddField(
            model_name='contentsection',
            name='section_type',
            field=models.CharField(choices=[('t', 'text'), ('s', 'spot'), ('i', 'image')], default='t', max_length=1),
        ),
    ]
