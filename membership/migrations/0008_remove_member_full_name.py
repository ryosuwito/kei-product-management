# Generated by Django 2.0.6 on 2018-06-16 19:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0007_member_full_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='full_name',
        ),
    ]
