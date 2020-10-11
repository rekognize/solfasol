# Generated by Django 3.1.1 on 2020-10-04 18:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0009_auto_20200918_0020'),
        ('shop', '0003_auto_20201004_2109'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'cart',
                'verbose_name_plural': 'carts',
            },
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveSmallIntegerField(default=1)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.cart', verbose_name='cart')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.item', verbose_name='item')),
            ],
        ),
        migrations.CreateModel(
            name='CartIssue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveSmallIntegerField(default=1)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.cart', verbose_name='cart')),
                ('issue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='issues.issue', verbose_name='issue')),
            ],
        ),
        migrations.AddField(
            model_name='cart',
            name='issues',
            field=models.ManyToManyField(blank=True, through='shop.CartIssue', to='issues.Issue'),
        ),
        migrations.AddField(
            model_name='cart',
            name='items',
            field=models.ManyToManyField(blank=True, through='shop.CartItem', to='shop.Item'),
        ),
        migrations.AddField(
            model_name='order',
            name='cart',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.cart', verbose_name='cart'),
        ),
    ]