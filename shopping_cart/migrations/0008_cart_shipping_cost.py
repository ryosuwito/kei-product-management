# Generated by Django 2.0.6 on 2018-07-22 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping_cart', '0007_auto_20180722_1904'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='shipping_cost',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
