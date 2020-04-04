# Generated by Django 3.0.4 on 2020-04-04 07:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0002_auto_20200402_0116'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='pinned',
            field=models.BooleanField(default=False, verbose_name='pinned'),
        ),
        migrations.AddField(
            model_name='series',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='content.Category', verbose_name='category'),
        ),
        migrations.AlterField(
            model_name='content',
            name='image',
            field=models.ImageField(upload_to='content/', verbose_name='image'),
        ),
    ]
