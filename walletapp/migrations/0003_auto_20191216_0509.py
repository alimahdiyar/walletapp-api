# Generated by Django 2.1.9 on 2019-12-16 05:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('walletapp', '0002_auto_20191216_0457'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='receiver',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='sender',
        ),
    ]