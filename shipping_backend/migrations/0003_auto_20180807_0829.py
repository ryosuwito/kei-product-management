# Generated by Django 2.0.6 on 2018-08-07 08:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shipping_backend', '0002_auto_20180722_1907'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shippingorigin',
            old_name='nama',
            new_name='name',
        ),
    ]