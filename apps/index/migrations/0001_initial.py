# Generated by Django 2.2.6 on 2019-11-01 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_title', models.CharField(default='', max_length=50, verbose_name='产品标题')),
                ('product_price', models.FloatField(max_length=11, verbose_name='产品价格')),
                ('number', models.IntegerField(max_length=11, verbose_name='刷单数量')),
                ('brush_price', models.FloatField(max_length=11, verbose_name='刷单价格')),
                ('key_word', models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='关键词')),
            ],
            options={
                'verbose_name': '产品信息',
                'verbose_name_plural': '产品信息',
            },
        ),
    ]
