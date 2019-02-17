# Generated by Django 2.0.6 on 2018-08-08 03:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database_wilayah', '0002_auto_20180612_1725'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kecamatan',
            name='kota',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='kecamatan_kota', to='database_wilayah.Kota'),
        ),
        migrations.AlterField(
            model_name='kelurahan',
            name='kecamatan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='kelurahan_kecamatan', to='database_wilayah.Kecamatan'),
        ),
        migrations.AlterField(
            model_name='kota',
            name='provinsi',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='kota_provinsi', to='database_wilayah.Provinsi'),
        ),
    ]
