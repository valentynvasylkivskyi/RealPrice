# Generated by Django 3.0.4 on 2020-04-22 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0016_auto_20200422_1459'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_name',
            field=models.CharField(default='Untracked', max_length=256),
        ),
    ]
