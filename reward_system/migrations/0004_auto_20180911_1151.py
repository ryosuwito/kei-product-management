# Generated by Django 2.0.6 on 2018-09-11 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reward_system', '0003_auto_20180911_1148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reward',
            name='current_point',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='reward',
            name='lifetime_point',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
