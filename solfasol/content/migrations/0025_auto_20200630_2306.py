# Generated by Django 3.0.7 on 2020-06-30 20:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contributors', '0001_initial'),
        ('content', '0024_content_new_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='contributors',
            field=models.ManyToManyField(blank=True, related_name='content_set', through='content.ContentContributor', to='contributors.Contributor', verbose_name='contributor'),
        ),
        migrations.AlterField(
            model_name='contentcontributor',
            name='contributor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contributors.Contributor', verbose_name='contributor'),
        ),
        migrations.DeleteModel(
            name='Contributor',
        ),
    ]
