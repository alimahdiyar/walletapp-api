# Generated by Django 2.2.4 on 2019-10-10 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sms', '0006_auto_20190623_1410'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'verbose_name': 'Message', 'verbose_name_plural': 'Messages'},
        ),
        migrations.AlterField(
            model_name='message',
            name='message',
            field=models.CharField(help_text='Message Text', max_length=500, verbose_name='Message Text'),
        ),
        migrations.AlterField(
            model_name='message',
            name='to',
            field=models.CharField(help_text='Recipient of the message', max_length=15, verbose_name='Recipient of the message'),
        ),
        migrations.AlterField(
            model_name='operator',
            name='api_endpoint',
            field=models.CharField(help_text='API Endpoint', max_length=500, verbose_name='API Endpoint'),
        ),
        migrations.AlterField(
            model_name='operator',
            name='name',
            field=models.CharField(help_text='A name for the operator', max_length=255, verbose_name='Operator Name'),
        ),
        migrations.AlterField(
            model_name='operator',
            name='password',
            field=models.CharField(help_text='Password given by operator', max_length=255, verbose_name='Password'),
        ),
        migrations.AlterField(
            model_name='operator',
            name='retry_gap_time',
            field=models.IntegerField(help_text='Time in minutes before you can try to send a message again', verbose_name='Retry Gap Time'),
        ),
        migrations.AlterField(
            model_name='operator',
            name='sender',
            field=models.CharField(help_text='The operator phone number', max_length=15, verbose_name='Sender Phone Number'),
        ),
        migrations.AlterField(
            model_name='operator',
            name='username',
            field=models.CharField(help_text='User name given by operator', max_length=255, verbose_name='Username'),
        ),
    ]
