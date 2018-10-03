# Generated by Django 2.0.6 on 2018-07-20 01:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shopping_cart', '0004_anonymouscart'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnonymousWishlist',
            fields=[
                ('wishlist_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='shopping_cart.WishList')),
                ('anon_user', models.CharField(db_index=True, help_text='Nama Anon', max_length=200)),
            ],
            bases=('shopping_cart.wishlist',),
        ),
    ]
