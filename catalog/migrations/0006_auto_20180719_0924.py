# Generated by Django 2.0.6 on 2018-07-19 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_auto_20180612_0940'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='photo_alt1',
            field=models.ImageField(blank=True, help_text='Foto Produk Alternatif 1', null=True, upload_to='product_photo'),
        ),
        migrations.AddField(
            model_name='product',
            name='photo_alt2',
            field=models.ImageField(blank=True, help_text='Foto Produk Alternatif 2', null=True, upload_to='product_photo'),
        ),
        migrations.AddField(
            model_name='product',
            name='photo_alt3',
            field=models.ImageField(blank=True, help_text='Foto Produk Alternatif 3', null=True, upload_to='product_photo'),
        ),
        migrations.AddField(
            model_name='product',
            name='photo_alt4',
            field=models.ImageField(blank=True, help_text='Foto Produk Alternatif 4', null=True, upload_to='product_photo'),
        ),
        migrations.AddField(
            model_name='product',
            name='photo_alt5',
            field=models.ImageField(blank=True, help_text='Foto Produk Alternatif 5', null=True, upload_to='product_photo'),
        ),
    ]