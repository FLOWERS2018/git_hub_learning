# Generated by Django 2.0 on 2018-08-20 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0007_auto_20180820_1123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='content',
            field=models.TextField(verbose_name='咨询详情'),
        ),
    ]