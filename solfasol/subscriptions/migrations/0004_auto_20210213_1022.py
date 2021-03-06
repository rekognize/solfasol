# Generated by Django 3.1.2 on 2021-02-13 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0003_auto_20210116_2326'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubscriptionType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('amount', models.PositiveSmallIntegerField()),
                ('description', models.TextField(blank=True, null=True)),
                ('payment_link', models.URLField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='subscriptions/')),
            ],
        ),
        migrations.AlterField(
            model_name='subscription',
            name='type',
            field=models.CharField(choices=[('dijital', 'Dijital abonelik - 100 TL'), ('yillik', 'Normal abonelik - 150 TL'), ('destekci', 'Destekçi abonelik - 300 TL'), ('yurtdisi', 'Yurtdışı abonelik - 300 TL'), ('duble', 'Çifte Destekçi abonelik - 600 TL'), ('yasasin', 'Yaşasın SOLFASOL! aboneliği - 1000 TL')], default='destekci', max_length=10, verbose_name='Abonelik türü'),
        ),
    ]
