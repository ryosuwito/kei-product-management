# Generated by Django 2.0.6 on 2018-07-19 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0014_auto_20180713_0221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='bank_name',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]