# Generated by Django 3.0.7 on 2020-07-03 12:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sessions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'cart',
                'verbose_name_plural': 'carts',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True, verbose_name='name')),
                ('slug', models.SlugField(editable=False, unique=True)),
                ('order', models.PositiveSmallIntegerField(blank=True, default=0, null=True, verbose_name='order')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
                'ordering': ('order',),
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('slug', models.SlugField(editable=False, unique=True)),
                ('description', models.CharField(max_length=250, verbose_name='description')),
                ('price', models.PositiveIntegerField()),
                ('image', models.ImageField(upload_to='shop/', verbose_name='image')),
                ('available', models.BooleanField(default=True, verbose_name='available')),
                ('promoted', models.BooleanField(default=False, verbose_name='promoted')),
                ('added', models.DateTimeField(auto_now_add=True, verbose_name='date')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.Category', verbose_name='category')),
            ],
            options={
                'verbose_name': 'item',
                'verbose_name_plural': 'items',
                'ordering': ('-added',),
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='name')),
            ],
            options={
                'verbose_name': 'tag',
                'verbose_name_plural': 'tags',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Full name')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('gsm_number', models.CharField(blank=True, max_length=20, null=True, verbose_name='Phone number')),
                ('identity_number', models.CharField(max_length=11, verbose_name='Identity number')),
                ('address', models.CharField(max_length=200, verbose_name='Address')),
                ('city', models.CharField(max_length=50, verbose_name='City')),
                ('country', models.CharField(max_length=50, verbose_name='Country')),
                ('zipcode', models.CharField(max_length=6, verbose_name='Zip code')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='notes')),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('cart', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.Cart', verbose_name='cart')),
            ],
        ),
        migrations.CreateModel(
            name='ItemAlternative',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=250, verbose_name='description')),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='price')),
                ('available', models.BooleanField(default=True, verbose_name='available')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Item')),
            ],
            options={
                'verbose_name': 'alternative',
                'verbose_name_plural': 'alternatives',
            },
        ),
        migrations.AddField(
            model_name='item',
            name='tags',
            field=models.ManyToManyField(blank=True, to='shop.Tag', verbose_name='tags'),
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added', models.DateTimeField(auto_now_add=True, verbose_name='date')),
                ('paid', models.BooleanField(default=False, verbose_name='paid')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Cart', verbose_name='cart')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Item', verbose_name='item')),
            ],
        ),
        migrations.AddField(
            model_name='cart',
            name='items',
            field=models.ManyToManyField(through='shop.CartItem', to='shop.Item'),
        ),
        migrations.AddField(
            model_name='cart',
            name='session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sessions.Session', verbose_name='session'),
        ),
    ]
