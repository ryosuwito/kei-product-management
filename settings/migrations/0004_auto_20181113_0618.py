# Generated by Django 2.0.8 on 2018-11-13 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0003_auto_20181112_1108'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='footerlink',
            name='link',
        ),
        migrations.RemoveField(
            model_name='headerlink',
            name='link',
        ),
        migrations.AddField(
            model_name='footerlink',
            name='addr',
            field=models.CharField(default='/', max_length=400),
        ),
        migrations.AddField(
            model_name='footerlink',
            name='is_left',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='footerlink',
            name='name',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='headerlink',
            name='addr',
            field=models.CharField(default='/', max_length=400),
        ),
        migrations.AddField(
            model_name='headerlink',
            name='name',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='headerlink',
            name='pos',
            field=models.PositiveIntegerField(editable=False, null=True, unique=True),
        ),
        migrations.DeleteModel(
            name='Link',
        ),
    ]
