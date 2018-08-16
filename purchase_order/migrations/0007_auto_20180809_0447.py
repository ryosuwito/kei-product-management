# Generated by Django 2.0.6 on 2018-08-09 04:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0010_remove_product_origin'),
        ('purchase_order', '0006_auto_20180809_0439'),
    ]

    operations = [
        migrations.CreateModel(
            name='PurchaseOrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(blank=True, null=True)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product_in_order', to='catalog.Product')),
            ],
            options={
                'verbose_name_plural': 'items in Order',
            },
        ),
        migrations.RemoveField(
            model_name='purchaseorder',
            name='cart',
        ),
        migrations.AddField(
            model_name='purchaseorderitem',
            name='purchases_order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='item_in_order', to='purchase_order.PurchaseOrder'),
        ),
    ]
