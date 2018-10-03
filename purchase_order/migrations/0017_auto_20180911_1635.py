# Generated by Django 2.0.6 on 2018-09-11 16:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0023_customer'),
        ('purchase_order', '0016_purchaseorderitem_product_referal'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchaseorder',
            name='shipping_address',
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='membership.Customer'),
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='is_set_as_dropship',
            field=models.BooleanField(default=False),
        ),
    ]
