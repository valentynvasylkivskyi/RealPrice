# Generated by Django 3.0.4 on 2020-04-22 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0017_auto_20200422_1523'),
    ]

    operations = [
        migrations.AlterField(
            model_name='price',
            name='date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
