# Generated by Django 2.0.6 on 2018-09-11 17:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reward_system', '0007_auto_20180911_1736'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reward',
            name='current_purchasing',
        ),
    ]
