# Generated by Django 2.0.6 on 2018-07-22 19:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shopping_cart', '0006_auto_20180721_1129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wishlist',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users_wishlist', to=settings.AUTH_USER_MODEL),
        ),
    ]