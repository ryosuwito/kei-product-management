# Generated by Django 2.0.6 on 2018-09-11 16:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0023_customer'),
        ('shopping_cart', '0014_auto_20180911_0919'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='membership.Customer'),
        ),
        migrations.AddField(
            model_name='cart',
            name='is_set_as_dropship',
            field=models.BooleanField(default=False),
        ),
    ]
