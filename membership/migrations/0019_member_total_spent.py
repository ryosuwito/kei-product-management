# Generated by Django 2.0.6 on 2018-08-17 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0018_auto_20180722_0614'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='total_spent',
            field=models.IntegerField(blank=True, editable=False, null=True),
        ),
    ]