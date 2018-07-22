# Generated by Django 2.0.6 on 2018-07-21 15:19

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0016_auto_20180721_1517'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='phone_number',
            field=models.CharField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(message="Nomor Telepon Harus memiliki format +62819999999 atau 0819999999'. Maksimal 15 Digit.", regex='^\\+?62?\\d{9,15}$')]),
        ),
    ]
