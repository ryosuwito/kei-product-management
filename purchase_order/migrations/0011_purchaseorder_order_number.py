# Generated by Django 2.0.6 on 2018-08-09 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchase_order', '0010_purchaseorder_total_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaseorder',
            name='order_number',
            field=models.CharField(blank=True, db_index=True, max_length=12),
        ),
    ]