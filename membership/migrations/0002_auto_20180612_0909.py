# Generated by Django 2.0.6 on 2018-06-12 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='guest',
            name='sponsor',
        ),
        migrations.RemoveField(
            model_name='guest',
            name='user',
        ),
        migrations.AlterField(
            model_name='member',
            name='bank_account_number',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='bank_book_photo',
            field=models.ImageField(blank=True, upload_to='bank_book_photo'),
        ),
        migrations.AlterField(
            model_name='member',
            name='bank_name',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='member',
            name='home_address',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='member',
            name='ktp_address',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='member',
            name='ktp_number',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='ktp_photo',
            field=models.ImageField(blank=True, upload_to='ktp_photo'),
        ),
        migrations.AlterField(
            model_name='member',
            name='member_type',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(0, 'guest'), (1, 'new member'), (2, 'dropshiper'), (3, 'reseller'), (4, 'agen'), (5, 'distributor'), (6, 'master seller')]),
        ),
        migrations.AlterField(
            model_name='member',
            name='profile_photo',
            field=models.ImageField(blank=True, upload_to='profile_photo'),
        ),
        migrations.AlterField(
            model_name='member',
            name='referal_code',
            field=models.CharField(blank=True, max_length=12),
        ),
        migrations.AlterField(
            model_name='member',
            name='sponsor_code',
            field=models.CharField(blank=True, max_length=12),
        ),
        migrations.DeleteModel(
            name='Guest',
        ),
    ]
