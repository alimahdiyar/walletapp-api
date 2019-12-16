# Generated by Django 2.1.9 on 2019-12-16 05:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('walletapp', '0004_transaction_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='user_transactions', to='walletapp.UserProfile'),
            preserve_default=False,
        ),
    ]