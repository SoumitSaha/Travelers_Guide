# Generated by Django 2.2.2 on 2019-06-23 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Places', '0004_verification'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='offday',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]
