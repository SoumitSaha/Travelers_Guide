# Generated by Django 2.2.2 on 2019-07-23 23:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Places', '0016_auto_20190723_2207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='placesuggestion',
            name='closing_time',
            field=models.CharField(blank=True, max_length=8, null=True),
        ),
        migrations.AlterField(
            model_name='placesuggestion',
            name='opening_time',
            field=models.CharField(blank=True, max_length=8, null=True),
        ),
    ]
