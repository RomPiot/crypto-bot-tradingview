# Generated by Django 4.0.2 on 2022-04-04 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crypto', '0015_alter_exchange_limit'),
    ]

    operations = [
        migrations.AddField(
            model_name='symbol',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
