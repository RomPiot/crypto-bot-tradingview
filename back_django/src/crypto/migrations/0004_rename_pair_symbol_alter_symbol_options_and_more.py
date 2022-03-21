# Generated by Django 4.0.2 on 2022-03-21 00:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crypto', '0003_rename_historic_historical_alter_historical_options'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Pair',
            new_name='Symbol',
        ),
        migrations.AlterModelOptions(
            name='symbol',
            options={'ordering': ['-created_at'], 'verbose_name': 'Symbol'},
        ),
        migrations.RenameField(
            model_name='historical',
            old_name='close_amount',
            new_name='close',
        ),
        migrations.RenameField(
            model_name='historical',
            old_name='close_datetime',
            new_name='datetime',
        ),
        migrations.RenameField(
            model_name='historical',
            old_name='open_amount',
            new_name='open',
        ),
        migrations.RenameField(
            model_name='historical',
            old_name='pair',
            new_name='symbol',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='pair',
            new_name='symbol',
        ),
        migrations.RemoveField(
            model_name='historical',
            name='open_datetime',
        ),
    ]
