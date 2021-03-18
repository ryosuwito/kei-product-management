# Generated by Django 2.0.6 on 2018-08-08 05:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shipping_backend', '0004_shippingorigin_is_default'),
        ('catalog', '0008_category_origin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='origin',
        ),
        migrations.AddField(
            model_name='product',
            name='origin',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shipping_backend.ShippingOrigin'),
        ),
    ]