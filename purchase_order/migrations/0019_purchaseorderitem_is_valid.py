# Generated by Django 2.0.6 on 2018-10-04 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchase_order', '0018_purchaseorder_is_valid'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaseorderitem',
            name='is_valid',
            field=models.BooleanField(db_index=True, default=True),
        ),
    ]
