# Generated by Django 4.0.2 on 2022-04-02 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crypto', '0013_symbol_last_imported_day'),
    ]

    operations = [
        migrations.AddField(
            model_name='exchange',
            name='limit',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
