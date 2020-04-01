# Generated by Django 3.0.4 on 2020-03-31 13:24

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import martor.models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0021_auto_20200330_1952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='added',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='date'),
        ),
        migrations.AlterField(
            model_name='article',
            name='body',
            field=martor.models.MartorField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='related_articles',
            field=models.ManyToManyField(blank=True, related_name='_article_related_articles_+', to='articles.Article', verbose_name='related articles'),
        ),
        migrations.AlterField(
            model_name='article',
            name='series',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='articles.Series', verbose_name='series'),
        ),
    ]