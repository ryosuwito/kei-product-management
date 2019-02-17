# Generated by Django 2.0.8 on 2018-11-13 06:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog_page', '0003_auto_20181112_1023'),
        ('settings', '0005_auto_20181113_0620'),
    ]

    operations = [
        migrations.AddField(
            model_name='footerlink',
            name='page',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog_page.Page'),
        ),
        migrations.AddField(
            model_name='headerlink',
            name='page',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog_page.Page'),
        ),
    ]
